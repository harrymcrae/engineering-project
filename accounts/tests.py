from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

# Create your tests here.

class PlayerUserTests(TestCase):
    
    def setUp(self): #this creates a player to test
        self.username = "player1"
        self.password = "password123"
        self.user = User.objects.create_user(username=self.username, password=self.password)
        
    def test_user_registration(self): #tests if a user can register
        user_count = User.objects.count()
        new_user = User.objects.create_user(username="newplayer", password="newpassword123")
        self.assertEqual(User.objects.count(), user_count + 1)  # Checks if the user count increased

    def test_user_login(self):
        login = self.client.login(username=self.username, password=self.password)
        self.assertTrue(login) #Tests if login works 
    
    def test_user_dashboard_access(self): #This sees if a player can access dashboard after logging in
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse("dashboard")) 
        self.assertEqual(response.status_code, 200)

    def test_non_authenticated_user_redirected(self): #This checks that a user who doesnt have access to the dashboard gets redirected to login 
        response = self.client.get(reverse("dashboard"))
        self.assertRedirects(response, '/accounts/login/?next=/dashboard/')

    def test_incorrect_login(self): #Tests if a user can login with incorrect password 
        login = self.client.login(username=self.username, password="wrongpassword")
        self.assertFalse(login)  # Login should fail

        response = self.client.post(reverse("login"), {"username": self.username, "password": "wrongpassword"})
        self.assertEqual(response.status_code, 200) 


class RegistrationTests(TestCase):

    def test_successful_registration(self):
        # This Tests if  a new user can register successfully."""
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!',
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful registration
        self.assertTrue(User.objects.filter(username='newuser').exists())  # Check user exists

    def test_registration_with_mismatched_passwords(self): #This tests if the confirmed password matches with the password first written
        response = self.client.post(reverse('register'), {
            'username': 'user1',
            'password1': 'password123!',
            'password2': 'wrongpassword!',
        })
        self.assertEqual(response.status_code, 200)  
        self.assertContains(response, "The two password fields didn’t match.")  # Check error message
        self.assertFalse(User.objects.filter(username='user1').exists())  # User should NOT be created

    def test_registration_with_duplicate_username(self):#Tests whether a username can be registered twice
        User.objects.create_user(username="existinguser", password="password123!")  # Create existing user
        response = self.client.post(reverse('register'), {
            'username': 'existinguser',
            'password1': 'NewPassword123!',
            'password2': 'NewPassword123!',
        })
        self.assertEqual(response.status_code, 200)  
        self.assertContains(response, "A user with that username already exists.")  # Check error message

    def test_registration_with_weak_password(self): #Tests how whether a weak password can be created
        response = self.client.post(reverse('register'), {
            'username': 'weakuser',
            'password1': '123',
            'password2': '123',
        })
        self.assertEqual(response.status_code, 200)  
        self.assertContains(response, "This password is too short.")  # Django’s built-in error
        self.assertFalse(User.objects.filter(username='weakuser').exists())  # User should NOT be created
    
    def test_registration_with_short_password(self): #Test that a password less than 8 characters is rejected
        response = self.client.post(reverse('register'), {
            'username': 'shortpassuser',
            'password1': 'short1!',
            'password2': 'short1!',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This password is too short.")
        self.assertFalse(User.objects.filter(username='shortpassuser').exists())  

    def test_registration_with_numeric_password(self): #Test that a password cannot be all numbers
        response = self.client.post(reverse('register'), {
            'username': 'numericpassuser',
            'password1': '12345678',
            'password2': '12345678',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This password is entirely numeric.") 
        self.assertFalse(User.objects.filter(username='numericpassuser').exists())  

    def test_registration_with_missing_password(self): #Test that a password cannot be empty
        response = self.client.post(reverse('register'), {
            'username': 'nopassworduser',
            'password1': '',
            'password2': '',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required.")  
        self.assertFalse(User.objects.filter(username='nopassworduser').exists())  


        
