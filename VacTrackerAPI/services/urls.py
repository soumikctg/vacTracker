from django.contrib import admin
from django.urls import path, include
from .views import RegisterView, LoginView, UserDataView, LogoutView, UserVaccineView, VacInfoWithoutLoginView, VaccinatorView, VacUpdateView

urlpatterns = [
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('user', UserDataView.as_view()),
    path('logout', LogoutView.as_view()),
    path('userVac', UserVaccineView.as_view()),
    path('vacInfoWithoutLogin', VacInfoWithoutLoginView.as_view()),
    path('vacUpdatePage', VaccinatorView.as_view()),
    path('vacUpdate', VacUpdateView.as_view()),
]