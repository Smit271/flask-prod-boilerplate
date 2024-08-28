class CustomMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        # Extracting information from the WSGI environment
        method = environ.get('REQUEST_METHOD')
        path = environ.get('PATH_INFO')
        api_key = environ.get('HTTP_API_KEY')

        print('Before request')
        print(f"===> Method: {method}")
        print(f"===> Path: {path}")
        print(f"===> API KEY: {api_key}")

        def custom_start_response(status, headers):
            # Code to execute before response
            return start_response(status, headers)

        # Call the original WSGI application
        return self.app(environ, custom_start_response)
