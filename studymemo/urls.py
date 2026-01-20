from django.contrib import admin
from django.urls import path, include
from memos import views as memo_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/signup/", memo_views.signup, name="signup"),
    path("accounts/", include("django.contrib.auth.urls")),  # login/logout
    path("", include("memos.urls")),
]
