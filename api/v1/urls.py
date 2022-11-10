from django.urls import path, include
from rest_framework.routers import DefaultRouter
from wallet.views import TransactionAPIViewset
from user.views import UserApiViewset, UserLoginViewset

router = DefaultRouter()
router.register('trans', TransactionAPIViewset, basename='trans')
router.register('user', UserApiViewset)

urlpatterns = [
    path('user/login/', UserLoginViewset.as_view({"post": "create"})),
    path('', include(router.urls)),
]
