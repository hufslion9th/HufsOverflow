from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url

urlpatterns = [
    path("signup/", views.signup, name="name_signup"),
    # This 2 views are for allauth package which doent need any views and has login/logout views already implemented.
    # path('login/', auth_views.LoginView.as_view(template_name='userauth/login.html'), name='name_login_req'),
    # path('logout/', auth_views.LogoutView.as_view(template_name='userauth/logout.html'), name='name_logout_req'),
    path("login/", views.login_request, name="name_login_req"),
    path("logout/", views.logout_request, name="name_logout_req"),
    path("editprofile/", views.editprofile, name="name_editprofile"),
    url(
        r"^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,32})/$",
        views.activate,
        name="activate",
    ),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="userauth/password_reset.html"), name='reset_password'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='userauth/password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="userauth/password_reset_confirm.html"), name="password_reset_confirm"),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="userauth/password_reset_complete.html"), name="password_reset_complete"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
