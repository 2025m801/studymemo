from django.urls import path
from . import views

urlpatterns = [
    path("", views.memo_list, name="memo_list"),                    
    path("memos/<int:pk>/", views.memo_detail, name="memo_detail"), 
    path("memos/new/", views.memo_create, name="memo_create"),      
    path("memos/<int:pk>/edit/", views.memo_update, name="memo_update"), 
    path("memos/<int:pk>/delete/", views.memo_delete, name="memo_delete"), 
    path("subjects/new/", views.subject_create, name="subject_create"),
    path("api/memos/<int:pk>/favorite/", views.memo_favorite_toggle, name="memo_favorite_toggle"),
    path("api/study-tip/", views.study_tip_api, name="study_tip_api"),
]
