from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('core.urls')),
    path('api-auth/', include('rest_framework.urls')),  # For browsable login
]


from rest_framework.authtoken.views import obtain_auth_token

urlpatterns += [
    path('api/token/', obtain_auth_token),
]
