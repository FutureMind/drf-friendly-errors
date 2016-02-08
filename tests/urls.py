from django.conf.urls import url

from tests import views, exceptions

urlpatterns = [
    url(r'^snippets/$', views.SnippetList.as_view(), name='snippet-list'),
    url(r'^snippets2/$', views.SnippetList.as_view(), name='snippet2-list'),
    url(r'^snippet/(?P<pk>\d+)/$', views.SnippetDetail.as_view(),
        name='snippet-detail'),

    url(r'^server_error/$', exceptions.server_error, name='server-error'),
    url(r'^not_found/$', exceptions.not_found, name='not-found'),
    url(r'^method_not_allowed/$', exceptions.method_not_allowed,
        name='not-allowed'),
    url(r'^not_authenticated/$', exceptions.not_authenticated,
        name='not-authenticated'),
]
