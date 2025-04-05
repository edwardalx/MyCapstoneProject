from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import PropertyApiViewset,UnitApiViewset,ImageApiViewset
from my_properties import views
router = DefaultRouter()
router.register(r'property',PropertyApiViewset)
router.register(r'unit',UnitApiViewset)
router.register(r'image',ImageApiViewset)




urlpatterns = [
path('api/', include(router.urls)),
path('api/v1/property/', view=views.ListView.as_view(), name='list-property'),
path('api/v1/property/<int:pk>/', view=views.DetailView.as_view(), name='retrieve-property'),
path('api/v1/property/create', view=views.CreateView.as_view(), name='create-property'),
path('api/v1/property/update/<int:pk>/', view=views.UpdateView.as_view(), name='update-property'),
path('api/v1/property/delete/<int:pk>/', view=views.DeleteView.as_view(), name='delete-property'),

]