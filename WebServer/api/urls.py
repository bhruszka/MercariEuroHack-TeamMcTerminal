from django.conf.urls import url, include
from rest_framework import routers

from api import views

router = routers.DefaultRouter()

user_router = routers.DefaultRouter()
user_router.register(r'^user', views.UserViewSet, base_name='administrator-designers')


app_name = 'api'
urlpatterns = [
    url('^api/', include([
        url(r'^login/$', views.LoginApiView.as_view(), name='login'),
        url(r'^login-facebook/$', views.LoginFacebookView.as_view(), name='login-facebook'),
        url(r'^logout/$', views.LogoutApiView.as_view(), name='logout'),
        url(r'^sign-in/$', views.CreateUser.as_view(), name='sign-in'),
        url(r'^', include(user_router.urls)),
    ]))
]

urlpatterns += [
    url(r'^', include(router.urls))
]
