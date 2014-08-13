from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^tea/', include('tea.foo.urls')),
    # (r'^tea/', include('tea.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

    (r'^thread/html/(?P<id>\w+)$', 'cmd.thread_html'),
    (r'^article/html/(?P<id>\w+)$', 'cmd.article_html'),
    (r'^shop/html/(?P<id>\w+)$', 'cmd.shop_html'),
    (r'^item/html/(?P<id>\w+)$', 'cmd.item_html'),
    (r'^question/html/(?P<id>\w+)$', 'cmd.question_html'),

    (r'^cmd/$', 'cmd.process'),
    (r'^save_file/$', 'cmd.save_file'),
)
