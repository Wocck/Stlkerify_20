from django.shortcuts import render
import logging

logger = logging.getLogger(__name__)


class ExceptionMiddleware(Exception):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
        except Exception as e:
            # Log your exception here
            logger.error(f"Exception caught by middleware: {e}")
            try:
                print("rendering")
                return render(request, "404.html", status=404)
            except Exception as e:
                logger.error(f"Error when rendering 404: {e}")
                print("raising e")
                raise e
        return response
