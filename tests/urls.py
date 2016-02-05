from django.conf.urls import url

from tests import views

urlpatterns = [
    url(r'^snippets/$', views.SnippetList.as_view(), name='snippet-list'),
    url(r'^snippets2/$', views.SnippetList.as_view(), name='snippet2-list'),
    url(r'^snippet/(?P<pk>\d+)/$', views.SnippetDetail.as_view(),
        name='snippet-detail')
]
