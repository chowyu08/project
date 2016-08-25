from django.conf.urls import url

from views import *

urlpatterns = [
    url(r'^$', index),
    url(r'^getSeeds/(?P<env>[a-zA-Z0-9_\-]+)/(?P<site>[a-zA-Z0-9_\-]+)/(?P<city>[a-zA-Z0-9_\-]+)/$', getSeeds),
    url(r'^download/(?P<component>[a-zA-Z0-9_\-]+)/(?P<filename>.+)/$', fileDownload),
    url(r'^getList/(?P<filename>.+)/$', getList),
    url(r'^getType/(?P<filename>.+)/$', getType),
]