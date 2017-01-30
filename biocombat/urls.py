from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('biocombat.views',
    # Examples:
    # url(r'^$', 'biocombat.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'index'),
    url(r'^uploadCard/$', 'uploadCard'),
    url(r'^openCard/', 'openCard'),
    url(r'^createCard/$', 'createCard'),
    url(r'^removeCardView/', 'removeCardView'),
    url(r'^removeCard/$', 'removeCard')
)
