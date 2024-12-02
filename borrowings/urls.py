from rest_framework.routers import DefaultRouter
from .views import BorrowingViewSet

router = DefaultRouter()
router.register(r"borrowings", BorrowingViewSet, basename="borrowing")

urlpatterns = router.urls

app_name = "borrowings"