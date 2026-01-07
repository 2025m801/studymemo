from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.urls import path
from .views import PostListAPIView
from django.conf import settings

urlpatterns = [
    path("", views.timeline, name='timeline'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post_create', views.post_create, name='post_create'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('api/posts/', PostListAPIView.as_view()),
    path('api/weather/', views.weather, name='weather'),
    path("ask/", views.chat_view, name="chat"),
    path("ask_api/", views.ask_gemini, name="ask_gemini"),


]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns