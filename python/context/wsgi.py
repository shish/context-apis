import context.api as ctx


class ContextMiddleware(object):
    def __init__(self, app, log_url):
        self.app = app
        self.log_url = log_url

    def __call__(self, environ, start_response):
        name = environ.get("PATH_INFO", "") + "?" + environ.get("QUERY_STRING", "")
        active = not name.startswith("/static/")

        if active:
            ctx.set_log(self.log_url)
            ctx.set_profile(True)
            ctx.log_bmark(name)

        response = self.app(environ, start_response)

        if active:
            ctx.set_profile(False)
        return response
