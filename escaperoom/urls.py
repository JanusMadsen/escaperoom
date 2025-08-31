"""
URL configuration for escaperoom project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from escapeapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('mushroom/', views.mushroom_puzzle, name='mushroom_puzzle'),
    path('sourdough/', views.sourdough_puzzle, name='sourdough_puzzle'),
    path('boardgames/', views.boardgame_puzzle, name='boardgame_puzzle'),
    path('berlin/', views.berlin_half_puzzle, name='berlin_half_puzzle'),
    path('summerhouse/final/', views.summerhouse_final, name='summerhouse_final'),
    path('summerhouse/', views.summerhouse_landing, name='summerhouse_landing'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
