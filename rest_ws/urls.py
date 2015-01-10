from django.conf.urls import patterns, include, url
from django.contrib import admin
from api.views import MyRESTView, MyConverterFromLocalView, MyConverterFromYoutubeView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'rest_ws.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'webclient.views.home', name='home'),
)

# urlpatterns += patterns('',
#     # this URL passes resource_id in **kw to MyRESTView
#     url(r'^api/v1.0/resource/(?P<resource_id>\d+)[/]?$', MyRESTView.as_view(), name='my_rest_view'),
#     url(r'^api/v1.0/resource[/]?$', MyRESTView.as_view(), name='my_rest_view'),
# )

urlpatterns += patterns('',
    # this URL passes resource_id in **kw to MyConverterView
    url(r'^api/v1.0/converter[/]?$', MyConverterFromLocalView.as_view(), name='my_converter_from_local_view'),
    url(r'^api/v1.0/youtube-converter[/]?$', MyConverterFromYoutubeView.as_view(), name='my_converter_from_youtube_view'),
)