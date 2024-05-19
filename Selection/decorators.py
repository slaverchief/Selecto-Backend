from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from rest_framework.response import Response
from Selecto.settings import DEBUG
from .models import OptionChar


def catch_exceptions(f):
    def wrapper(self, request):
        if DEBUG:
            return f(self, request)
        else:
            try:
                return f(self, request)
            except IntegrityError:
                return Response({'status': 1, 'result': 'Вы нарушаете какое-то системное ограничение.'})
            except ObjectDoesNotExist:
                return Response({'status': 0, 'result': {}})
            except Exception as exc:
                return Response({'status': 2})
    return wrapper
