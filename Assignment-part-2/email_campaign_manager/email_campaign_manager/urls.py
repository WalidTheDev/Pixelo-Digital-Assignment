from django.contrib import admin
from django.urls import path
from campaigns import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dashboard, name='dashboard'),
    path('contacts/', views.contacts, name='contacts'),
    path('templates/', views.templates_view, name='templates'),
    path('campaigns/', views.campaigns_view, name='campaigns'),
    path('run-campaign/<int:campaign_id>/', views.run_campaign, name='run_campaign'),
]
