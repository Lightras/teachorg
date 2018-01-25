
from django.conf.urls import url
from .views import groups, loginq, registration, groupsdata

urlpatterns = [
    url(r'^groups/$', groups, name='groups'),
    url(r'^login/$', loginq, name='login'),
    url(r'^registration/$', registration, name='registration'),
    url(r'^groupsdata/$', groupsdata)
]
