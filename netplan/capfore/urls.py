from django.conf.urls import url, include
from capfore import views
#from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'tasks', views.TaskViewSet,'task')
router.register(r'packages',views.PackageThresholdViewSet)
router.register(r'citys',views.CityAttributeViewSet)
router.register(r'scenes',views.SceneAttributeViewSet)



urlpatterns = [
    url(r'^$' , views.list),
    url(r'^list/',views.list,name='capfore_tasklist'),
    url(r'^new/',views.new,name='capfore_tasknew'),
    url(r'^detail/(?P<pk>[0-9]+)$',views.detail,name='capfore_taskdetail'),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
