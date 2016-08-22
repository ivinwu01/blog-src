from django.conf.urls import url
import views
urlpatterns = [
    url(r'^$', views.index, name='home'),
    url(r'^login$', views.login),
    url(r'^lookblog$',views.lookblog),
    url(r'^say$',views.say),
    url(r'^share$',views.share),
    # url(r'^upimg$',load.upimg),
    # url(r'^upload$', load.upload),
]
