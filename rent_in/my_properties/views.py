
# Create your views here.
from django.shortcuts import render
from .models import Property,Unit,Image
from .serializers import PropertySerialzer,UnitSerialzer,ImageSerialzer
from rest_framework import viewsets,generics
from rest_framework import permissions
from rest_framework import filters
class PropertyApiViewset(viewsets.ModelViewSet):
    model = Property
    queryset = Property.objects.all()
    serializer_class = PropertySerialzer

class ListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Property.objects.all()
    serializer_class = PropertySerialzer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', ' author']
    ordering_fields = ['publication_year', 'author']
    

class DetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Property.objects.all()
    serializer_class = PropertySerialzer
                                
class CreateView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Property.objects.all()
    serializer_class = PropertySerialzer
class DeleteView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Property.objects.all()
    serializer_class = PropertySerialzer
class UpdateView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Property.objects.all()
    serializer_class = PropertySerialzer

class UnitApiViewset(viewsets.ModelViewSet):
    model = Unit
    queryset = Unit.objects.all()
    serializer_class = UnitSerialzer

class ImageApiViewset(viewsets.ModelViewSet):
    model = Image
    queryset = Image.objects.all()
    serializer_class = ImageSerialzer

