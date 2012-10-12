#define ctx_log_bmark(text) ctx_log_msg(__FUNCTION__, text, "BMARK")
#define ctx_log_start(text) ctx_log_msg(__FUNCTION__, text, "START")
#define ctx_log_endok(text) ctx_log_msg(__FUNCTION__, text, "ENDOK")
#define ctx_log_ender(text) ctx_log_msg(__FUNCTION__, text, "ENDER")
#define ctx_log_clear(text) ctx_log_msg(__FUNCTION__, text, "CLEAR")

extern void ctx_set_log(const char *name, const int append);
extern void ctx_log_msg(const char *func, const char *text, const char *type);
