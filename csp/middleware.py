class CspMiddleware(object):

    def process_response(self, request, response):
        response['X-Content-Security-Policy'] = "allow 'self'"
        return response
