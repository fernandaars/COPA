from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$',
        views.index, name='index'),
    url(r'^welcome/$',
        views.welcome, name='welcome'),
    url(r'^containers_list/$',
        views.containers_list, name='containers_list'),
    url(r'^containers_list/start/(?P<xhost>[\w\-]+)/(?P<container_name>[\w\-]+)$',
        views.containers_start, name='containers_start'),
    url(r'^containers_list/stop/(?P<xhost>[\w\-]+)/(?P<container_name>[\w\-]+)$',
        views.containers_stop, name='containers_stop'),
    url(r'^containers_list/delete/(?P<xhost>[\w\-]+)/(?P<container_name>[\w\-]+)$',
        views.containers_delete, name='containers_delete'),
    url(r'^containers_list/freeze/(?P<xhost>[\w\-]+)/(?P<container_name>[\w\-]+)$',
        views.containers_freeze, name='containers_freeze'),
    url(r'^containers_list/unfreeze/(?P<xhost>[\w\-]+)/(?P<container_name>[\w\-]+)$',
        views.containers_unfreeze, name='containers_unfreeze'),
    url(r'^containers_list/new/$',
        views.containers_new, name='containers_new'),
    url(r'^containers_list/add/$',
        views.containers_add, name='containers_new'),
    url(r'^containers_list/console/(?P<server>[\w\-]+)/(?P<container_name>[\w\-]+)$',
        views.containers_terminal, name='containers_terminal'),
    url(r'^containers_list/migrate/(?P<origin>[\w\-]+)/(?P<name_container>[\w\-]+)/(?P<destination>[\w\-]+)$',
        views.containers_migrate, name='containers_migrate'),
    url(r'^containers_list/info/(?P<xhost>[\w\-]+)/(?P<container_name>[\w\-]+)$',
        views.containers_info, name='containers_info'),
    url(r'^containers_list/api/$',
        views.api_execution, name='api_execution'),
]
