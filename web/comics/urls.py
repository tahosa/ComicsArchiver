from django.conf.urls import url
from web.comics import views

urlpatterns = [
    url(r'', views.comics_list)
]
