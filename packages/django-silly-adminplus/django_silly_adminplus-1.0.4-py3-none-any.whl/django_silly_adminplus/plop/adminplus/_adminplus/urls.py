from django.urls import path
from . import views


# the url patterns are automaticaly included in the main urls.py within the namespace 'adminplus',
# do not change this.

urlpatterns = [
    path('dsap/adminplus/', views.adminplus, name='adminplus'),
]
