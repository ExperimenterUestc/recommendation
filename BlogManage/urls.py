from django.conf.urls import patterns, include, url
from .views import WriteRank,ReadUserRank,PublicFilm,ManageRank,FilmSearch,Recommend
urlpatterns = patterns('BlogManage.views',
                       #     url(r'^login/$', 'user.LoginUser', name='loginurl'),
#     url(r'^logout/$', 'user.LogoutUser', name='logouturl'),
url(r'write/$', WriteRank, name='blog_write'),
url(r'search/$', FilmSearch,name='film_search'),
url(r'read/(?P<username>[a-zA-Z0-9]+)/$', ReadUserRank, name='film_read'),
url(r'public/$', PublicFilm, name='public_article'),
url(r'manage/$', ManageRank, name='film_manage'),
url(r'recommend/$',Recommend, name='film_recommend'),
)
