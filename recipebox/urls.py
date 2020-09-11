"""recipebox URL Configuration

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
from django.urls import path
from homepage import views
urlpatterns = [
    path('', views.index, name='homepage'),
    path('recipe/<int:recipe_id>', views.recipe),
    path('author/<int:author_id>', views.author),
    path('recipe/<int:recipe_id>/edit/', views.recipe_edit_view, name='edit'),
    path('favorites/<int:recipe_id>/', views.favorites_view, name='favorites'),
    path('addauthor/', views.add_author),
    path('addrecipe/', views.add_recipe),
    path('login/', views.login_view),
    path('logout/', views.logout_view),
    path('admin/', admin.site.urls),
]
