import json


class AppClass:
    def __init__(self, environ, start_response):
        self.environ = environ
        self.start = start_response

    def __iter__(self):
        status = '200 OK'
        response_headers = [('Content-type', 'text/plain')]
        self.start(status, response_headers)

        method = self.environ.get('REQUEST_METHOD')
        query_string = self.environ.get('QUERY_STRING')

        body = self.environ.get('wsgi.input')
        if self.environ.get('CONTENT_LENGTH', 0):
            input = body.read()
        else:
            input = ''

        output = f'{method} {query_string}\n{input}'

        yield bytes(output, encoding='utf-8')


application = AppClass
