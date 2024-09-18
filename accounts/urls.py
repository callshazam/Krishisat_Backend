from django.urls import path
from .views import FarmerRegistrationView, StaffRegistrationView,UserLoginView, LogoutView

urlpatterns = [
    path('register/farmer/', FarmerRegistrationView.as_view(), name='register-farmer'),
    path('register/staff/', StaffRegistrationView.as_view(), name='register-staff'),
    path('login/', UserLoginView.as_view(), name='token_obtain_pair'),
    path('logout/', LogoutView.as_view(), name='logout'),

]
