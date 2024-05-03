from django.urls import path
from . import views
from .views import UserRegisterView, UserEditView, PasswordsChangeView, ShowProfilePageView, EditProfilePageView, \
    CreateProfilePageView
from .views import MyPasswordResetView, MyPasswordResetDoneView,MyPasswordResetCompleteView


urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('edit_profile/', UserEditView.as_view(), name='edit_profile'),
    path('password/', PasswordsChangeView.as_view(template_name='registration/password_change.html'),
         name='password_change'),
    path('password_succes', views.password_success, name='password_success'),
    path('<int:pk>/profile/', ShowProfilePageView.as_view(), name='show_profile_page'),
    path('<int:pk>/edit_profile_page/', EditProfilePageView.as_view(), name='edit_profile_page'),
    path('create_profile_page/', CreateProfilePageView.as_view(), name='create_profile_page'),
    path('profile/<int:pk>/', ShowProfilePageView.as_view(), name='profile_page'),
    path('reset_password/', MyPasswordResetView.as_view(), name='password_reset'),
    path('reset_password/done/', MyPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/done/', MyPasswordResetCompleteView.as_view(), name='password_reset_complete'),


]
