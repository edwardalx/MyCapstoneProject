# MyCapstoneProject
# Rentin App

##  What Has Been Achieved

- **Models, Forms, and Serializers:**  
  Implemented core models for Tenants, Properties, Units, Payments, and related forms and serializers.

- **Frontend Templates:**  
  Created and rendered HTML templates to present property data and forms on the frontend.

- **API Development:**  
  Built RESTful APIs using Django REST Framework (DRF) for all core resources.

- **Unit Testing:**  
  Written tests for various API endpoints to validate their behavior and functionality.

##  Areas for Improvement

1. Improve frontend URLs to be more relatable (user-friendly)
2. Investigate how to allow users to select a property and unit on the frontend and proceed to payment
3. Design and implement a working payment system
4. Add validation so that `tenant.user.username` only accepts numbers (in forms and serializers)
5. Add additional logic for room availability, notifications, etc.
6. Improve frontend templates and styling (UI/UX)
7. Learn and apply how to consume your own API from the frontend
8. Configure a custom domain (e.g., `www.rentinapp.com`)
9. Gather user feedback and implement suggested improvements
10. Conduct further testing to boost confidence in app stability and performance







 <!-- def test_Unit_CreateView(self):
        # Ensure 'room_number' is a string and 'property' is the ID of an existing property.
        data = { 
            'property': 1,  # This should be the ID of an existing property.
            'room_number': '1',  # Ensure this is a string (since room_number is a CharField).
            'cost': 2000, 
            'max_no_of_people': 2 
        }
        
        response = self.client.post('/property/api/unit/', data)
        
        # Print the response data to understand the error
        print(response.status_code)
        print(response.data)
        
        # Check if the response code is 201 (Created)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED) -->