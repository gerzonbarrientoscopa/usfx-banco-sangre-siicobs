"""sucre_siicobs_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include, re_path
from django.http import HttpResponse
from graphene_django.views import GraphQLView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.utils import json
from django.conf.urls.static import static

from siicobs_main import settings


class AuthenticatedGraphQLView(GraphQLView):
  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAuthenticated]

  def authenticate_request(self, request):
    for auth_class in self.authentication_classes:
      auth_tuple = auth_class().authenticate(request)
      if auth_tuple:
        request.user, request.token = auth_tuple
        break

  def check_permissions(self, request):
    for permission_class in self.permission_classes:
      if not permission_class().has_permission(request, self):
        return False
    return True

  @method_decorator(csrf_exempt)
  def dispatch(self, request, *args, **kwargs):
    try:
      self.authenticate_request(request)
      has_permission = self.check_permissions(request)
      if not has_permission:
        return HttpResponse(
            json.dumps({'errors': ['permission denied']}),
            status=status.HTTP_403_FORBIDDEN,
            content_type='application/json')
    except AuthenticationFailed as auth_failed_error:
      return HttpResponse(
          json.dumps({
            'errors': [str(auth_failed_error)]
          }),
          status=status.HTTP_401_UNAUTHORIZED,
          content_type='application/json')
    return super(AuthenticatedGraphQLView, self).dispatch(request, *args, **kwargs)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('fronts.urls')),
    path('', include('users.urls')),
    path('', include('donors.urls')),
    path('', include('donations.urls')),
    path('', include('refreshments.urls')),
    path('', include('settings.urls')),
    path('', include('packages.urls')),
    path('', include('fragmentations.urls')),
    path('', include('laboratories.urls')),
    path('', include('distributions.urls')),
    path('', include('reports.urls')),
    path('', include('provisions.urls')),
    re_path(r'^api/v1/graphql', AuthenticatedGraphQLView.as_view(graphiql=True)),
    re_path(r'^api/v1/open/graphql', csrf_exempt(GraphQLView.as_view(graphiql=True))),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
