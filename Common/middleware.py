from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin


class ErrorHandlerMiddleware(MiddlewareMixin):

    def process_exception(self, request, exception):
        print("Error", exception)

        data = {
            "error": str(exception)
        }

        return JsonResponse(data, status=400)