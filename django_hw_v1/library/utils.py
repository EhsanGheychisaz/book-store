def compatibility_middleware(get_response):
    def middleware(request):
        if type(request.body) == bytes:
            request._body = request.body.decode('utf-8')
        if not hasattr(request, 'headers'):
            request.headers = HttpHeaders(request.META)
        return get_response(request)

    return middleware


class HttpHeaders(dict):
    def __init__(self, environ):
        headers = {}
        for k, v in environ.items():
            if k.startswith('HTTP_'):
                headers[k[5:].lower().replace('_', '-')] = v
            elif k in {"CONTENT_TYPE", "CONTENT_LENGTH"}:
                headers[k.lower().replace('_', '-')] = v
        super().__init__(headers)

    def __getitem__(self, key):
        return super().__getitem__(key.lower().replace('_', '-'))

    def get(self, key):
        try:
            return self[key]
        except KeyError:
            return None
