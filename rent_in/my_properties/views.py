
# Create your views here.
from django.shortcuts import render
from .models import Property,Unit,Image
from .serializers import PropertySerialzer,UnitSerializer,ImageSerialzer
from rest_framework import viewsets,generics
from rest_framework import permissions
from rest_framework import filters
from django.views.generic import TemplateView
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
    serializer_class = UnitSerializer

class UnitListApiView(generics.ListAPIView):
    model = Unit
    serializer_class = UnitSerializer

    def get_queryset(self):
        property_id = self.kwargs['property']  # get 'Papose Flats' from URL
        return Unit.objects.filter(property__id=property_id)


class ImageApiViewset(viewsets.ModelViewSet):
    model = Image
    queryset = Image.objects.all()
    serializer_class = ImageSerialzer

class SelectUnitView(TemplateView):
    template_name = 'accounts/unit_Img.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        property_id = self.kwargs.get('property_id')
        context['property_id'] = property_id  # <--- Add this
        context['units'] = Unit.objects.filter(property_id=property_id)
        return context
    
def unit_list(request, property_id):  # Remove self, **kwargs
    units = Unit.objects.filter(property_id=property_id)
    context = {
        "units": units,
        "is_authenticated": request.user.is_authenticated,
        'property_id': property_id,
    }
    return render(request, 'accounts/unit_Img.html', context)

def property_list(request):
    properties = Property.objects.all()
    return render(request, 'accounts/propertyImg.html', {'properties': properties})



