from django.http import HttpResponseRedirect, HttpResponseNotFound , response
from django.shortcuts import render ,reverse

# Create your views here.
from rest_framework import viewsets , generics
from rest_framework.decorators import detail_route
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from django.contrib.auth.models import User
from capfore.models import Task , PackageThreshold,  CityAttribute, SceneAttribute
from capfore.serializers import UserSerializer, TaskSerializer, CellSerializer ,\
    PackageThresholdSerializer, CityAttributeSerializer, SceneAttributeSerializer

from capfore.forms import  TaskForm , TaskInfoForm
from capfore.tasks import forecast

import logging
logger = logging.getLogger(__name__)

def index(request):
    return list(request)

def list(request):
    return render(request, 'capfore/list.html')

def detail(request , pk):
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        pass
    if request.method == 'GET':
        form = TaskForm
        content = {
            'form' : form,
            'taskid' : pk,
        }
        print ('begin render')
        return render(request, 'capfore/detail.html',content)

def new(request):
    if request.method =='POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            curdate = form.cleaned_data['curdate']
            period = form.cleaned_data['period']
            print (request.user,type(request.user))
            owner = User.objects.get(username=request.user)
            newtask = Task(name=name,curdate=curdate,period=period,owner=owner)
            newtask.save()
            forecast.delay(newtask.id)
            return HttpResponseRedirect(reverse('capfore_tasklist'))
    form = TaskForm()
    return render(request, 'capfore/new.html', {'newform': form})



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# class CellsView(generics.GenericAPIView):
#     queryset = Task.objects.all()
#     serializer_class = CellSerializer
#
#     def get(self, request, *args, **kwargs):
#         task = self.get_object()
#         serializer = self.get_serializer(task.cells.all())
#         return Response(serializer.data)
#


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


    @detail_route()
    def cells(self,request,*args,**kwargs):
        queryset = self.get_object().cells.all()
        page = self.paginate_queryset(queryset)
        if 'csv' in request.accepted_media_type : page = None
        if page is not None:
            serializer = CellSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = CellSerializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        user = self.request.user
        return Task.objects.filter(owner=user)


class PackageThresholdViewSet(viewsets.ModelViewSet):
    queryset = PackageThreshold.objects.all()
    serializer_class = PackageThresholdSerializer

class CityAttributeViewSet(viewsets.ModelViewSet):
    queryset = CityAttribute.objects.all()
    serializer_class = CityAttributeSerializer

class SceneAttributeViewSet(viewsets.ModelViewSet):
    queryset = SceneAttribute.objects.all()
    serializer_class = SceneAttributeSerializer

