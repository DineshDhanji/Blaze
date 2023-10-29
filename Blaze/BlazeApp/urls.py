from django.urls import path

from . import views

urlpatterns = [
    path('', views.newsfeed, name='newsfeed')
]

handler404 = 'BlazeAdministration.views.page_not_found_404'
