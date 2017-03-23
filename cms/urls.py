from django.conf.urls import url
import load
urlpatterns = [
    url(r'^$', load.index, name='home'),
    url(r'^update$',load.update),
    url(r'^blogsList$', load.blogsList),
    url(r'^logout$', load.logout),
    url(r'^classification$', load.classification),
    url(r'^column$', load.column),
]
