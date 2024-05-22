from django.http import Http404
import logging

from library_management.settings import DEBUG

logger = logging.getLogger("librarymanagement")


def access_permission(allowed_account_types: list):
    def access_permission_decorator(func):
        def wrapper(request, *args, **kwargs):
            if request.user.type not in allowed_account_types:
                raise Http404
            return func(request, *args, **kwargs)

        return wrapper

    return access_permission_decorator


def capture_exception_logs(func):
    def wrapper(*args, **kwargs):
        try:
            a = func(*args, **kwargs)
            print("Execution finished | Status: Success")
            return a

        except Exception as err:
            if isinstance(err, Http404) or DEBUG:
                print("Execution finished | Status: Exception Handled (404)")
                raise err

            logger.error(f"{func.__name__}: Unexpected error occurred.")
            logger.error(f"{func.__name__}: {err}")
            print("Execution finished | Status: Unhandled Exception")

    return wrapper
