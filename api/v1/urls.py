from django.urls import include, path
from rest_framework.routers import DefaultRouter

from user.views import UserApiViewset, UserLoginViewset, UserStats
from wallet.views import TransactionAPIViewset

router = DefaultRouter()
router.register('transaction', TransactionAPIViewset, basename='transaction')
router.register('user', UserApiViewset)

urlpatterns = [
    path('user/stats/', UserStats.as_view({"get": "list"})),
    path('user/login/', UserLoginViewset.as_view({"post": "create"})),
    path('', include(router.urls)),
]
