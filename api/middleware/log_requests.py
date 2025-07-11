import logging
import time

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        method = request.method
        path = request.get_full_path()
        ip = request.META.get('REMOTE_ADDR')

        response = self.get_response(request)

        duration = time.time() - start_time
        status_code = response.status_code

        logger.info(f"[{ip}] {method} {path} => {status_code} ({duration:.2f}s)")

        return response
