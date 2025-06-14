"""
URL configuration for expense_calculator project.

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
from django.db import router
from django.urls import path, include
#create the router for expenses app
from rest_framework.routers import DefaultRouter
from expenses import views
# Import TemplateView
from django.views.generic import TemplateView  

router = DefaultRouter()
router.register('expenses', views.ExpenseViewSet, basename='expense')

urlpatterns = [
    # add api urls
    path('api/', include(router.urls)),
    # configure rest framework's browsable API
    path('api-auth/', include('rest_framework.urls')),
    path('admin/', admin.site.urls),
     # use templateview as_view to serve templates/index.html
    path('', TemplateView.as_view(template_name='index.html')),
]

admin.site.site_header = "Expense Calculator Admin"