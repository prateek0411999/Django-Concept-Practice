
from django.urls import path
from .views import article_list,article_detail, ArticleApiView,ArticleDetails

urlpatterns = [
    
    path('article/',article_list),
    path('detail/<int:pk>',article_detail),
    #bcoz ArticleApiView is a class that's why we are using as_view method
    path('classArticle/',ArticleApiView.as_view()),
    path('classDetail/<int:id>/',ArticleDetails.as_view())

]
