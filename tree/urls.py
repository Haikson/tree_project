from django.urls import path
from tree import views

appname='tree'

urlpatterns = [
    path('', views.TreeView.as_view(), name='tree_view'),
    path('json/', views.TreeJSONView.as_view(), name='tree_json_view'),
]