from django.conf.urls import url

from . import views

# Main URLS
urlpatterns = [url(r'^$', views.index, name='monitor_index'),
                url(r'^dashboard$', views.dashboard, name='dashboard')]

# Configuration URLS
urlpatterns += [url(r'^(?P<pk>\w+)$', views.ConfigurationDetailView.as_view(),
                    name='configuration_detail'),
                url(r'^configuration/create/$',
                    views.ConfigurationCreate.as_view(),
                    name='configuration_create'),
                url(r'^(?P<pk>\w+)/update$',
                    views.ConfigurationUpdate.as_view(),
                    name='configuration_update'),
                url(r'^(?P<pk>\w+)/delete$',
                    views.ConfigurationDelete.as_view(),
                    name='configuration_delete'),
                ]

# TierClass URLS
urlpatterns += [url(r"^tier/(?P<pk>\d+$)", views.TierClassDetailView.as_view(),
                    name="tierclass_detail"),
                url(r'^tier/create$', views.TierClassCreate.as_view(),
                    name='tierclass_create'),
                url(r'^tier/(?P<pk>\d+)/update$',
                    views.TierClassUpdate.as_view(), name='tierclass_update'),
                url(r'^tier/(?P<pk>\d+)/delete$',
                    views.TierClassDelete.as_view(), name='tierclass_delete'),
                ]

# Pool URLS
urlpatterns += [url(r"^locus/(?P<pk>\w+$)", views.LocusDetailView.as_view(),
                    name="locus_detail"),
                url(r'^locus/create/$', views.LocusCreate.as_view(),
                    name='locus_create'),
                url(r'^tier/(?P<pk>\d+)/create_locus$',
                    views.LocusCreate.as_view(), name='tier_locus_create'),
                url(r'^locus/(?P<pk>\w+)/update/$', views.LocusUpdate.as_view(),
                    name='locus_update'),
                url(r'^locus/(?P<pk>\w+)/delete/$', views.LocusDelete.as_view(),
                    name='locus_delete'),
                ]
