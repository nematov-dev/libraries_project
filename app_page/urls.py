from django.urls import path

from app_page.views import InfoTemplateView

app_name = 'infos'
urlpatterns = [
    path('',InfoTemplateView.as_view(),name='info'),
]