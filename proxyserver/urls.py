from django.conf.urls import patterns, include, url
from proxyserver.app.api.host import *
from proxyserver.app.main.dispatcher import *

urlpatterns = patterns('',
                       url(r'^host/$', host_all),
                       url(r'^host/(\d+)/$', host_by_id),
                       url(r'^account/$', dispatcher)
                       )
