from django.urls import path
from .views import SignUpView


app_name = 'univ_interests'
urlpatterns = [
    path('sign-up/', SignUpView.as_view(), name='sign-up')
]
