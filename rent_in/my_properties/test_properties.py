import django
django.setup()

from django.urls import reverse
from rest_framework import status
# from api.views import ListView
from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from .models import Property, Unit, Image

User = get_user_model()

class APITestCase(TestCase):
    def setUp(self):
        print('Start Test')
        self.client = APIClient()
        self.property = Property.objects.create(name="The Grundle", location='OCE Campus', no_of_units = 40, cost_of_rent = 2000, availability = 0 )
        self.unit = Unit.objects.create(property=self.property, room_number = 1, cost = 2000, max_no_of_people = 2)
        self.image = Image.objects.create(property = self.property, unit = self.unit, description = 'Fron view of the grundle', photo = None)

        self.user = User.objects.create(username="Ed")
        self.user.set_password("Edward@alx2025")
        self.user.save()

        self.client.force_authenticate(user=self.user)
        # self.client.login(username="Ed", password="Edward@alx2025")  Only needed when you have @login_required
        print()
      
    def tearDown(self):
        print('After Test')
        print("\n")
        
    def test_PropertyCreateView(self):
       data = { 'name':"Talbot", 'location':'OCE Campus', 'no_of_units' : 12, 'cost_of_rent' : 3000, 'availability' : 1 }
       response = self.client.post('/property/api/property/', data)
       self.assertEqual(response.status_code, status.HTTP_201_CREATED)
       print(response.data)
    
    def test_Property_url_in_test(self):
        url = reverse('create-property')  # Replace 'create_book' with your URL name
        response = self.client.get(url)
        print(response.status_code)

    def test_Property_ListViews(self):
        response = self.client.get('/property/api/property/', )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.status_code)
        print(response.data)

    def test_Property_DetailView(self):
        response = self.client.get(f'/property/api/property/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)

    def test_Property_UpdateView(self):
        data = {"title": "MummyReturnsEdward"}
        response = self.client.patch(f'/property/api/property/{self.property.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_Property_DeleteView(self):
        response = self.client.delete(f'/property/api/property/{self.property.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT )
        print(response.status_code)


    # def test_Unit_CreateView(self):
    #    data = { 'property':self.property.id, 'room_number' : 1, 'cost' : 2000, 'max_no_of_people' : 2 }
    #    response = self.client.post('/property/api/unit/', data)
    #    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #    print(response.data)
    
    def test_Unit_url_in_test(self):
        url = reverse('update-property', kwargs={'pk': self.property.id})  # Replace 'create_book' with your URL name
        response = self.client.get(url)
        print(response.status_code)

    def test_Unit_ListViews(self):
        response = self.client.get('/property/api/unit/', )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.status_code)
        print(response.data)

    def test_Unit_DetailView(self):
        response = self.client.get(f'/property/api/unit/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)

    def test_Unit_UpdateView(self):
        data = {"title": "MummyReturnsEdward"}
        response = self.client.patch(f'/property/api/unit/{self.unit.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_Unit_DeleteView(self):
        response = self.client.delete(f'/property/api/unit/{self.unit.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT )
        print(response.status_code)


    # def test_Image_CreateView(self):
    #    data = { 'property' : self.property.id, 'unit' : self.unit.id, 'description' : 'Fron view of the grundle', 'photo' : '' }
    #    response = self.client.post('/property/api/image/', data)
    #    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #    print(response.data)
    
    def test_Image_url_in_test(self):
        url = reverse('retrieve-property', kwargs={'pk': self.property.id})  # Replace 'create_book' with your URL name
        response = self.client.get(url)
        print(response.status_code)

    def test_Image_ListViews(self):
        response = self.client.get('/property/api/image/', )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.status_code)
        print(response.data)

    def test_Image_DetailView(self):
        response = self.client.get(f'/property/api/image/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)

    def test_Image_UpdateView(self):
        data = {"title": "MummyReturnsEdward"}
        response = self.client.patch(f'/property/api/image/{self.image.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_Image_DeleteView(self):
        response = self.client.delete(f'/property/api/image/{self.image.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT )
        print(response.status_code)
   
