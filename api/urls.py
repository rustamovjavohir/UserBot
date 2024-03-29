from django.urls import path, include

from api.staff.views.views import *

from api.staff.urls import urlpatterns as staff_urls
from api.authorization.urls import urlpatterns as authorization_urls
from api.checking.urls import urlpatterns as checking_urls
from api.files.urls import urlpatterns as files_urls
from api.authorization.views.views import LoginPage

urlpatterns = [
    path('files/', include('api.files.urls')),
]

urlpatterns += staff_urls
urlpatterns += authorization_urls
urlpatterns += checking_urls
