
from django.conf.urls import url
from .views import groups, loginq, registration, groupsdata, schedule, subjects, semesters, logoutq

urlpatterns = [
    url(r'^login/$', loginq, name='login'),
    url(r'^registration/$', registration, name='registration'),
    url(r'^logout/$', logoutq),

    url(r'^schedule/$', schedule),
    url(r'^groups/$', groups, name='groups'),
    url(r'^subjects/$', subjects),
    url(r'^semesters/$', semesters),

    url(r'^groupsdata/$', groupsdata),
]
