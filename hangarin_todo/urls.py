from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

admin.site.site_header = "Hangarin Admin"
admin.site.site_title  = "Hangarin To-Do Manager"
admin.site.index_title = "Welcome to Hangarin Administration"

urlpatterns = [
    path('admin/', admin.site.urls),

    # PWA routes (manifest.json, serviceworker.js)
    path('', include('pwa.urls')),

    # Allauth (Google / social login)
    path('accounts/', include('allauth.urls')),

    # Standard Django login / logout
    path('login/',  auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # All app routes
    path('', include('tasks.urls')),
]