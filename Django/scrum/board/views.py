from django.shortcuts import render
from rest_framework import viewsets, authentication, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Sprint, Task
from .serializers import SprintSerializer, TaskSerializer, UserSerializer
from .filters import TaskFilter, SprintFilter
from django.contrib.auth import get_user_model
# Create your views here.

User = get_user_model()

class DefaultsMixin(object):
    '''Default settings for view authentication, permissions, filtering and pagination.'''
    authentication_classes = [
        authentication.BasicAuthentication,
        authentication.TokenAuthentication,
    ]
    permission_classes = [
        permissions.IsAuthenticated    
    ]
    paginate_by = 25
    paginate_by_param = 'page_size'
    max_paginate_by = 100
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

class SprintViewSet(DefaultsMixin, viewsets.ModelViewSet):
    queryset = Sprint.objects.order_by('end')
    serializer_class = SprintSerializer
    search_fields = ['name',]
    ordering_fields = ['end', 'name',]
#    filter_class = SprintFilter

class TaskViewSet(DefaultsMixin, viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_class = TaskFilter
    search_fields = ['name', 'description',]
    ordering_fields = ['name', 'order', 'started', 'due', 'completed',]


class UserViewSet(DefaultsMixin, viewsets.ModelViewSet):
    lookup_field = User.USERNAME_FIELD
    lookup_url_kwarg = User.USERNAME_FIELD
    queryset = User.objects.order_by(User.USERNAME_FIELD)
    serializer_class = UserSerializer
    search_fields = [User.USERNAME_FIELD,]