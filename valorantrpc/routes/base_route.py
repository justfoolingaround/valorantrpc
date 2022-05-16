class Route:
    def __init__(self, method, url):

        self.method = method
        self.url = url

    def __call__(self, method=None, endpoint=None):

        if method is None:
            method = self.method

        def pre_decorator(f):
            def wrapper(session, *args, **kwargs):
                return f(
                    session,
                    session.request(
                        method, self.url + (endpoint or ""), *args, **kwargs
                    ),
                    *args,
                    **kwargs
                )

            return wrapper

        return pre_decorator

    def act(self, session, *args, endpoint=None, **kwargs):
        return session.request(
            self.method, self.url + (endpoint or ""), *args, **kwargs
        )

    def extend(self, method, url):
        return Route(method, self.url + url)
