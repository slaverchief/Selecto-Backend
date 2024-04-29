from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from rest_framework.response import Response


def catch_exceptions(f):
    def wrapper(self, request):
        try:
            return f(self, request)
        except IntegrityError:
            return Response({'status': "Some constraint is violated"})
        except ObjectDoesNotExist:
            return Response({'status': f'Object doesnt exist'})
        except Exception as exc:
            return Response({'status': str(exc)})
    return wrapper
