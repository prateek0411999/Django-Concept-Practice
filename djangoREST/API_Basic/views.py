from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import Article
from rest_framework.parsers import JSONParser
from .serializers import ArticleSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import mixins
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated 

from rest_framework import viewsets
from django.shortcuts import get_object_or_404

# Create your views here.



#this is the function based views 
#we do have class based view that is what we basically use 
@api_view(['GET','POST'])
def article_list(request):
    if request.method == 'GET':
        articles = Article.objects.all()
        #serialize the articles so that it could be readable
        serializer= ArticleSerializer(articles, many=True)
       # return JsonResponse(serializer.data , safe=False)
        return Response(serializer.data)

    elif request.method == 'POST':
        #data = JSONParser().parse(request)
                                        #data=data
        serializer = ArticleSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT','DELETE'])
def article_detail(request,pk):
    try: 
        article= Article.objects.get(pk=pk)
    
    except Article.DoesNotExist:
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'GET':
        serializer= ArticleSerializer(article)
        #return JsonResponse(serializer.data)
        return Response(serializer.data)
    elif request.method == 'PUT':
        #data= JSONParser().parse(request)
        serializer= ArticleSerializer(article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            #return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#this is about the function based views

#REST framework  provides an APIView Class which subclasses Django's View Class
#APIView classes are different from regular View classes 
#Requests passed to the handler methods will be REST framework's Request instance not like the Django httprequest

                        #CLASS BASED API VIEW

#this class extends the APIView class from the rest framework so we are passing it in like this
class ArticleApiView(APIView):
    def get(self, request):
        articles = Article.objects.all()
        serializer= ArticleSerializer(articles, many=True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ArticleDetails(APIView):
    def get_object(self,id):
        try:
            return Article.objects.get(id=id)
        except Article.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    def get(self, request,id ):
        article = self.get_object(id)
        serializer= ArticleSerializer(article)
        return Response(serializer.data)

    def put(self, request, id):
        article=self.get_object(id)
        serializer= ArticleSerializer(article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        article= self.get_object(id)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


        #we also have GENERICS VIEWS

class GenericAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):     
    serializer_class= ArticleSerializer
    queryset = Article.objects.all()
    
    #authentication_classes=[SessionAuthentication, BasicAuthentication]
    #first it will check for the session auth then the basic authentication
    authentication_classes=[TokenAuthentication]
    permission_classes= [IsAuthenticated]

    lookup_field = 'id'
    #if we have used pk in put and delete then we don't have to use the lookup_field 
    
    def get(self, request):
        return self.list(request)
    
    def post(self, request):
        return self.create(request)
    
    def put(self,request, id=None):
        return self.update(request,id)
    
    def delete(self,request,id=None):
        return self.destroy(request, id)


#if we use this type of view set then
#we need to all the functionality by ourself
class ArticleViewSet(viewsets.ViewSet):
    def list(self, request):
        article = Article.objects.all()
        serializer= ArticleSerializer(article, many=True)
        return Response(serializer.data)

    def create(self, request):
        
        serializer= ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #for update we have retrieve
    def retrieve(self, request ,pk=None):
        queryset = Article.objects.all()
        article= get_object_or_404(queryset ,pk=pk)
        serializer= ArticleSerializer(article)
        return Response(serializer.data)

    def update(self, request, pk=None):
        article=Article.objects.get(pk=pk)
        serializer= ArticleSerializer(article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #we need to bind this to url now
    #the best way is to use routers

#WE ALSO HAVE THE GENERIC VIEW SET 
#where we need to make use of mixins

class GenericViewSet(viewsets.GenericViewSet, mixins.ListModelMixin,mixins.CreateModelMixin,mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin):
    serializer_class=ArticleSerializer
    queryset = Article.objects.all()