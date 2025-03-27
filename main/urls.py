from django.urls import path
from .views import *


# app_name = 'main'  # here for namespacing of urls.

urlpatterns = [
    path("", homepage, name="homepage"),
    path('send_otp/', send_otp, name='send_otp'),
    path('accounts/login/', send_otp, name='send_otp'),
    path('verify/', verify_otp, name='verify_otp'),
    path('dashboard/', dashboard, name='dashboard'),
    path('logout/', logout_user, name='logout'),
    path('update-profile/', update_profile, name='update_profile'),

]