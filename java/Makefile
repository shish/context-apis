
all: output.java.ctxt output.java-profile.ctxt

output.java.ctxt:   Example.class Context.class
	java Example

output.java-profile.ctxt: ExampleProfile.class libcontext.so
	java -agentpath:./libcontext.so=output.java-profile.ctxt,ExampleProfile ExampleProfile

%.class: %.java
	javac $<

libcontext.so: java-profiler.c
	gcc -fPIC \
		-I `/usr/libexec/java_home`/include/ \
		-I `/usr/libexec/java_home`/include/darwin/ \
		-shared -o libcontext.so java-profiler.c
		# -shared -Wl,-soname,libcontext.so.1 -o libcontext.so java-profiler.c
