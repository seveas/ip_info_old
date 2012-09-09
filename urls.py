from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'web.ip_info.views.main'),
    url(r'^whois-ip/$', 'web.ip_info.views.whois_ip'),
    url(r'^whois-host/$', 'web.ip_info.views.whois_host'),
)
