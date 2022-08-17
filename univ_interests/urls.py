from django.urls import path
from .views import SignUpView, SignInView


app_name = 'univ_interests'
urlpatterns = [
    path('sign-up/', SignUpView.as_view(), name='sign-up'),
    path('sign-in/', SignInView.as_view(), name='sign-in')
]
