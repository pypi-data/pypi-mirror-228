
from django.urls import path, include
from django_silly_adminplus import views

from django_silly_adminplus.config import SILLY_ADMINPLUS as conf

app_name = 'adminplus'
urlpatterns = [
]

if not conf['USE_ADMINPLUS_APP']:
    urlpatterns += [
        path(conf['DSAP_PREFIX'] + 'adminplus/', views.adminplus, name='adminplus'),
    ]

if conf['USE_ADMINPLUS_APP']:
    urlpatterns += [
        path('', include('_adminplus.urls')),
    ]
