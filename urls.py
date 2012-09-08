from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'web.ip_info.views.main'),
)
