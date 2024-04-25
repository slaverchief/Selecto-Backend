from django.urls import path
from .views import *
from knox.views import LogoutView

urlpatterns = [
    path('selection', SelectionView.as_view()),
    path('char', CharView.as_view()),
    path('login', LoginView.as_view(), name='knox_login'),
    path('logout/', LogoutView.as_view(), name='knox_logout'),
]