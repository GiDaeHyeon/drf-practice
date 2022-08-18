from django.urls import path
from .views import (
    SignUpView,
    SignInView,
    UniversitySearchView,
    UniversityPreferenceDeleteView,
    UniversityPreferenceCreateView,
    UniversityRankingView
)


app_name = 'univ_interests'
urlpatterns = [
    path('sign-up/', SignUpView.as_view(), name='sign-up'),
    path('sign-in/', SignInView.as_view(), name='sign-in'),
    path('search/', UniversitySearchView.as_view(), name='search'),
    path('preference/delete/', UniversityPreferenceDeleteView.as_view(), name='prefer-delete'),
    path('preference/create/', UniversityPreferenceCreateView.as_view(), name='prefer-delete'),
    path('ranking/', UniversityRankingView.as_view(), name='ranking')
]
