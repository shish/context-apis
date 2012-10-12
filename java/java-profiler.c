#include <jvmti.h>
#include <jni.h>
#include <jni_md.h>
#include <stdio.h>
#include <string.h>
 
#include <time.h>
#include <sys/timeb.h>
#include <unistd.h>

static FILE *_context_log;
static char *_filter;
static int first_log_ok = 0;

static void check_jvmti_error(jvmtiEnv *jvmti, jvmtiError errnum, const char *str) {
    if(errnum != JVMTI_ERROR_NONE) {
        char       *errnum_str;
        errnum_str = NULL;
        (void)(*jvmti)->GetErrorName(jvmti, errnum, &errnum_str);
        printf("ERROR: JVMTI: %d(%s): %s\n", errnum, (errnum_str==NULL?"Unknown":errnum_str), (str==NULL?"":str));
    }
}

static void get_thread_name(jvmtiEnv *jvmti, jthread thread, char *tname, int maxlen) {
	jvmtiThreadInfo info;
	jvmtiError      error;

	(void)memset(&info,0, sizeof(info));
	(void)strcpy(tname, "Unknown");

	error = (*jvmti)->GetThreadInfo(jvmti, thread, &info);
	check_jvmti_error(jvmti, error, "Cannot get thread info");

	if ( info.name != NULL ) {
		int len;

		len = (int)strlen(info.name);
		if ( len < maxlen ) {
			(void)strcpy(tname, info.name);
		}

		error = (*jvmti)->Deallocate(jvmti, (unsigned char*)info.name);
	}
}

int filter(jvmtiEnv *env, jmethodID method) {
	jvmtiError error;
	jclass class;

	error = (*env)->GetMethodDeclaringClass(env, method, &class);

	char *signature;
	char *generic;
	error = (*env)->GetClassSignature(env, class, &signature, &generic);

	int match = 0;
	if(!strncmp(signature+1, _filter, strlen(_filter))) {
		match = 1;
	}

	error = (*env)->Deallocate(env, (unsigned char*)signature);
	error = (*env)->Deallocate(env, (unsigned char*)generic);

	return match;
}

void ctx_log_prof(jvmtiEnv *env, jthread thread, jmethodID method, char *type) {
	if(_context_log) {
		struct timeb tmb;
		char hostname[256];
		char threadname[256];

		if(!filter(env, method)) return;

		if(!first_log_ok) {
			first_log_ok = 1;
			ctx_log_prof(env, thread, method, "BMARK");
		}

		jvmtiError error;
		char *methodname;
		char *sig;
		char *gsig;
		error = (*env)->GetMethodName(env, method, &methodname, &sig, &gsig);
		check_jvmti_error(env, error, "Cannot get method info");

		ftime(&tmb);
		gethostname(hostname, 256);
		get_thread_name(env, thread, threadname, 256),

        fprintf(
			_context_log,
			"%ld.%d %s %d %s %s %s %s\n",
            tmb.time, tmb.millitm,
            hostname,
			getpid(),
			threadname,
            type, methodname, methodname
        );

		error = (*env)->Deallocate(env, (unsigned char*)methodname);
		error = (*env)->Deallocate(env, (unsigned char*)sig);
		error = (*env)->Deallocate(env, (unsigned char*)gsig);
	}
}

static void JNICALL cbMethodEntry(jvmtiEnv *env, JNIEnv* jni_env, jthread thread, jmethodID method){
	ctx_log_prof(env, thread, method, "START");
}

static void JNICALL cbMethodExit(jvmtiEnv *env, JNIEnv* jni_env, jthread thread, jmethodID method, jboolean was_popped_by_exception, jvalue return_value){
	ctx_log_prof(env, thread, method, was_popped_by_exception ? "ENDER" : "ENDOK");
}

jint Agent_OnLoad(JavaVM *vm, char *options, void *reserved){
	jvmtiEnv *env;
	jvmtiCapabilities capa;
	jvmtiError error;
	jint res;
	jvmtiEventCallbacks callbacks;
	int i;

	// noob string processing
	int commas = 0;
	char *opt2 = NULL;
	for(i=0; i<strlen(options); i++) {
		if(options[i] == ',') {
			commas++;
			options[i] = '\0';
			_filter = &options[i+1];
		}
	}
	if(commas != 1) {
		printf("Context requires two paramaters, log file and package filter\n");
		printf("Use a command line like this:\n");
		printf("java -agentpath:./libcontext.so=log_file.ctxt,net.mycompany. TestClass\n");
		return 1; //JNI_ERROR;
	}
	_context_log = fopen(options,"w");
	for(i=0; i<strlen(_filter); i++) {
		if(_filter[i] == '.') _filter[i] = '/';
	}

	res =  (*vm)->GetEnv(vm, (void**)&env, JVMTI_VERSION_1);

	(void)memset(&capa,0, sizeof(capa));
	capa.can_generate_method_entry_events = 1;
	capa.can_generate_method_exit_events = 1;
	(*env)->AddCapabilities(env, &capa);

	(void)memset(&callbacks,0, sizeof(callbacks));	     	    
	callbacks.MethodEntry  = &cbMethodEntry;
	callbacks.MethodExit   = &cbMethodExit; 
	error = (*env)->SetEventCallbacks(env, &callbacks, (jint)sizeof(callbacks));

	error = (*env)->SetEventNotificationMode(env, JVMTI_ENABLE, JVMTI_EVENT_METHOD_ENTRY, (jthread)NULL);
	error = (*env)->SetEventNotificationMode(env, JVMTI_ENABLE, JVMTI_EVENT_METHOD_EXIT, (jthread)NULL);

	return JNI_OK;	     	     
}

JNIEXPORT void JNICALL Agent_OnUnload(JavaVM *vm) {
	fflush(_context_log);
	fclose(_context_log);
}
