from django.conf.urls import url

from .functions import RestFunctions

# REST URLS
urlpatterns = [url(r"^locus/$", RestFunctions.locus,
                   name="locus"),
               url(r"^kpilink/$", RestFunctions.kpilink,
                   name="kpilink"),
               url(r"^kpiresource/$", RestFunctions.kpiresource,
                   name="kpiresource"),
               url(r"^kpiwireless/$", RestFunctions.kpiwireless,
                   name="kpiwireless"),
               url(r"^kpicommand/$", RestFunctions.kpicommand,
                   name="kpicommand"),
               url(r"^configuration/$", RestFunctions.update_configuration,
                   name="update_configuration"),
                url(r"^dashboard/$", RestFunctions.dashboard,
                name="network_dashboard"),
                url(r"^dashboardlinks/$", RestFunctions.dashboardlinks,
                name="network_dashboardlinks"),
               ]
