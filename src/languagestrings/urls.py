"""languagestrings URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from django.contrib.auth import views
from django.views.generic.base import RedirectView
from strings.views import UserViewSet, GroupViewSet, ProductViewSet, PRODUCTS, VIEWS, LOCALVIEWS
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'products', ProductViewSet)

for product, viewSet in VIEWS.iteritems():
    pattern = r'^'+str(product)
    router.register(pattern, viewSet, base_name=str(pattern))

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^languagestring/', include('strings.urls', namespace='languagestring')),
    url(r'^localtext/', include('strings.urls', namespace='localtext')),
    url(r'login/', views.login, kwargs={"template_name":'registration/login.html'}, name="Login"),
    url(r'logout/', views.logout, kwargs={"template_name":'registration/logout.html'}, name="Logout"),
    url(r'^/?$', RedirectView.as_view(url='/languagestring/', permanent=True)),
]

urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]