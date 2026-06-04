import threading

_thread_locals = threading.local()
# Utility function to get the current request from thread-local storage
def get_current_request():
    return getattr(_thread_locals, 'request', None)

class RequestMiddleware:
    '''Middleware to store the current request in thread-local storage.'''
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _thread_locals.request = request
        response = self.get_response(request)
        return response