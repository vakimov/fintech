from django.conf.urls import url, include
from rest_framework import routers
from credits import views

router = routers.DefaultRouter()
router.register(r'organisations', views.OrganizationViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]