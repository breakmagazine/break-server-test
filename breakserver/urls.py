from django.contrib import admin
from django.urls import path
from django.urls import include
from .views import kakao_login_page


urlpatterns = [
   path('', kakao_login_page, name='home'),
   path('admin/', admin.site.urls),
   path('accounts/', include('dj_rest_auth.urls')),
   path('accounts/', include('dj_rest_auth.registration.urls')),
   path('allauth/', include('allauth.urls')),
   path('accounts/', include('accounts.urls')),
   path('accounts/social/', include('allauth.socialaccount.urls')),
]
