from iblog.api.views import (LikeViewSet,  
	PostViewSet, CommentViewSet, ProfileViewSet 
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'LIKE', LikeViewSet)
router.register(r'PROFILE', ProfileViewSet)
router.register(r'POST', PostViewSet)
router.register(r'COMMENT', CommentViewSet)

urlpatterns = router.urls