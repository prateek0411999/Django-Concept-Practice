
from django.urls import path, include
from .views import article_list,article_detail, ArticleApiView,ArticleDetails, GenericAPIView, ArticleViewSet
from rest_framework.routers import DefaultRouter

#first need to create the obj of DefaultRouter and then register it
router= DefaultRouter()
router.register('article', ArticleViewSet, basename='article')

urlpatterns = [
    
    path('article/',article_list),
    path('detail/<int:pk>',article_detail),
    #bcoz ArticleApiView is a class that's why we are using as_view method
    path('classArticle/',ArticleApiView.as_view()),
    path('classDetail/<int:id>/',ArticleDetails.as_view()),
    path('generic/article/',GenericAPIView.as_view()),
    path('generic/article/<int:id>/',GenericAPIView.as_view()),

    path('viewset/',include(router.urls)),
     path('viewset/<int:pk>/',include(router.urls))
]
