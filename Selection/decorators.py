from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from rest_framework.response import Response
from Selecto.settings import DEBUG


def catch_exceptions(f):
    def wrapper(self, request):
        if DEBUG:
            return f(self, request)
        else:
            try:
                return f(self, request)
            except IntegrityError:
                return Response({'status': "Some constraint is violated"})
            except ObjectDoesNotExist:
                return Response({'status': 'success', 'result': {}})
            except Exception as exc:
                return Response({'status': str(exc)})
    return wrapper
