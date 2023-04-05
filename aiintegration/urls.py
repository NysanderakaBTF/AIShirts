from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.views import serve
from django.urls import path
from . import views

"""
-  /prompt-executor/ : Maps to the  PromptExecutor  view for POST requests. 
-  /prompt-executor/<int:pk>/ : Maps to the  PromptExecutor  view for GET and DELETE requests. 
-  /prompt-list/ : Maps to the  PromptListView  view. 
-  /model-scheduler/ : Maps to the  ModelSchedulerApiView  view for GET (list) and POST (create) requests. 
-  /model-scheduler/<int:pk>/ : Maps to the  ModelSchedulerApiView  view for GET (retrieve), PUT (update), and DELETE (destroy) requests. 
-  /ai-models/ : Maps to the  AiModelListCreateAPIView  view for listing and creating AI models. 
-  /ai-models/<int:pk>/ : Maps to the  AiModelRetrieveUpdateDeleteAPIView  view for retrieving, updating, and deleting AI models. 
 
"""

urlpatterns = [
    path('prompt/executor/', views.PromptExecutor.as_view(), name='prompt-executor'),
    path('prompt/i/<int:pk>/', views.PromptImageAPIView.as_view(), name='prompt-executor-detail'),
    path('prompt/', views.PromptListView.as_view(), name='prompt-list'),
    path('prompt/<int:pk>/', views.PromptDetailAPIView.as_view({'get':'retrieve', 'delete':'destroy', 'put':'update'}), name='prompt-detail'),
    path('model-scheduler/', views.ModelSchedulerApiView.as_view({'get': 'list', 'post': 'create'}),
         name='model-scheduler'),
    path('model-scheduler/<int:pk>/',
         views.ModelSchedulerApiView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}),
         name='model-scheduler-detail'),
    path('ai-models/', views.AiModelListCreateAPIView.as_view(), name='ai-models-list-create'),
    path('ai-models/<int:pk>/', views.AiModelRetrieveUpdateDeleteAPIView.as_view(),
         name='ai-models-retrieve-update-delete'),

]
