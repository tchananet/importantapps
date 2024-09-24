from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductModalViewset, CategoryModalViewset

router = DefaultRouter()
# router.register(r'',ProductModalViewset )
router.register(r'categories',CategoryModalViewset )

urlpatterns = [
    path("p", ProductModalViewset.as_view()),
    path('', include(router.urls)),
]
