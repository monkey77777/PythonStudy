"""blog_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import include , path
from rest_framework.documentation import include_docs_urls # 追加
from rest_framework.schemas import get_schema_view # 追加
from rest_framework_swagger.views import get_swagger_view # 追加

#schema_view = get_schema_view(title='Blog API') # 追加
API_TITLE = 'Blog API'
API_DESCRIPTION = 'A Web API for creating and editing blog posts.'
# schema_view = get_schema_view(title=API_TITLE) # 追加
schema_view = get_swagger_view(title=API_TITLE) # 追加


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('posts.urls')), #追加
    path('api-auth/', include('rest_framework.urls')),#追加
    path('api/v1/rest-auth/', include('rest_auth.urls')), # 追加
    path('api/v1/rest-auth/registration/',
         include('rest_auth.registration.urls')),
    path('docs/', include_docs_urls(title=API_TITLE,
                                    description=API_DESCRIPTION)),
    # path('schema/', schema_view), # 追加
    path('swagger-docs/', schema_view), # 追加
]
