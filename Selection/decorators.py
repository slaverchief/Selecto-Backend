from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from rest_framework.response import Response
from Selecto.settings import DEBUG
from .models import OptionChar
import re


def catch_exceptions(f):
    def wrapper(self, request):
        if DEBUG:
            return f(self, request)
        else:
            try:
                return f(self, request)
            except IntegrityError as exc:
                pattern = r'"(.+?)"'
                res = re.findall(pattern, str(exc))[1]
                return Response({'status': 1, 'result': f'Вы нарушаете системное ограничение: {res}'})
            except ObjectDoesNotExist:
                return Response({'status': 0, 'result': {}})
            except Exception as exc:
                return Response({'status': 2})
    return wrapper
