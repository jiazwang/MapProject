from django.conf.urls import url
from . import views

app_name = 'gallery'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^(?P<collection_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<picture_id>[0-9]+)/favorite/$', views.favorite, name='favorite'),
    url(r'^pictures/(?P<filter_by>[a-zA_Z]+)/$', views.pictures, name='pictures'),
    url(r'^create_collection/$', views.create_collection, name='create_collection'),
    url(r'^(?P<collection_id>[0-9]+)/create_picture/$', views.create_picture, name='create_picture'),
    url(r'^(?P<collection_id>[0-9]+)/delete_picture/(?P<picture_id>[0-9]+)/$', views.delete_picture, name='delete_pic'),
    url(r'^(?P<collection_id>[0-9]+)/favorite_collection/$', views.favorite_collection, name='favorite_collection'),
    url(r'^(?P<collection_id>[0-9]+)/delete_collection/$', views.delete_collection, name='delete_collection'),
]
