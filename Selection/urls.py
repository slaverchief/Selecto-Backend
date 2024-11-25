from django.urls import path
from .views import *

urlpatterns = [
    path('selection', SelectionView.as_view()),
    path('char', CharView.as_view()),
    path('option', OptionView.as_view()),
    path('optionchar', OptionCharView.as_view()),
    # path('user', UserAPIView.as_view()),
    path('calc', CalcView.as_view()),
]