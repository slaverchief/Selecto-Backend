from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from rest_framework.response import Response
from Selecto.settings import DEBUG
from .exceptions import CalcException
from .models import OptionChar
import re


def catch_exceptions(f):
    def wrapper(self, request):
        if DEBUG:
            return f(self, request)
        else:
            try:
                return f(self, request)
            except CalcException as exc:
                return Response(status=400, data={'detail': str(exc)})
            except IntegrityError as exc:
                pattern = r'"(.+?)"'
                res = re.findall(pattern, str(exc))[1]
                return Response(status=400, data={'detail': f'The constraint has been violated: {res}'})
            except ObjectDoesNotExist:
                return Response([])
            except Exception as exc:
                return Response(status=404)
    return wrapper
