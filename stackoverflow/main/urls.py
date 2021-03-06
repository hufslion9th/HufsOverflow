from django.contrib import admin
from django.urls import path
from django.conf import settings
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.questions, name="name_questions"),
    path("tag/<str:tag_word>/", views.questionByTag, name="name_questionByTag"),
    path("question/<int:pk>/", views.questionsingle, name="name_questionsingle"),
    path("askquestion/", views.askquestion, name="name_askquestion"),
    path("profile/<str:username>/", views.profile, name="name_profile"),
    path("question/<int:pk>/<int:pk2>/", views.is_accepted, name="name_is_accepted"),
    path("rule/",views.rule,name="rule"),
    path("searchResult/", views.searchResult, name='searchResult'),
    path("notice/",views.notice,name="notice"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
