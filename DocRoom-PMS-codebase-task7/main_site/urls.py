from django.urls import path, include
from . import views
from .views import SignUpView

urlpatterns = [
    path('', views.home, name='home'),
    path('add/', views.add_patient, name='add_patient'),
    path('display/', views.display_patient, name="display_patient"),
    path('display/update/<id>', views.update_patient_details, name="update_patient"),
    path("mail/<id>/", views.send_patient_email, name="send_email"),

    #-- White Code --
    path("accounts/", include("django.contrib.auth.urls")),
    path("signup/", SignUpView.as_view(), name="signup"),
    #-- White Code --

]