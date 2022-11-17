from django.urls import path, include
from rest_framework.routers import DefaultRouter
from wallet.views import TransactionAPIViewset
from user.views import UserApiViewset, UserLoginViewset, UserStats

router = DefaultRouter()
router.register('transaction', TransactionAPIViewset, basename='transaction')
router.register('user', UserApiViewset)

urlpatterns = [
    path('user/stats/', UserStats.as_view({"get": "list"})),
    path('user/login/', UserLoginViewset.as_view({"post": "create"})),
    path('', include(router.urls)),
]
