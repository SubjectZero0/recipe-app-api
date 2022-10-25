"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


from rest_framework import routers
from User.views import UserViewSet
from Recipe.views import RecipeApiViewset, MyRecipesApiViewset, TagsModelViewset, IngredientsModelViewset
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

router = routers.DefaultRouter()
router.register('users', UserViewSet, basename = 'users')
router.register('recipes',RecipeApiViewset, basename = 'recipes' )
router.register('my_recipes', MyRecipesApiViewset, basename='my_recipes')
router.register('tags', TagsModelViewset, basename = 'tags')
router.register('ingredients', IngredientsModelViewset, basename = 'ingredients')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('', include('User.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name = 'api-schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='api-schema'), name='api-docs'),

]

if settings.DEBUG:
    """
    Only in dev mode - Serve media files
    """
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root = settings.MEDIA_ROOT,
    )