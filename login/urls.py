from django.urls import path
from . import views
app_name='login'
urlpatterns = [
    path("sign_in", views.SignInView.as_view(), name="sign in"),
    path("sign_up", views.SignUpView.as_view(), name="sign up"),
]