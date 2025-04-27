from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from uuid import uuid4

# Create your tests here.
User = get_user_model() 

class AdminLoginTestCase(TestCase):
    def setUp(self):
        # Create a superuser (admin)
        self.admin_username = 'testadmin'
        self.admin_password = 'testpassword'
        User.objects.create_superuser(
            username=self.admin_username,
            email='admin@example.com',
            password=self.admin_password
        )

    def test_admin_login(self):
        response = self.client.post('/admin/login/?next=/admin/', {
            'username': self.admin_username,
            'password': self.admin_password
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/admin/')
        self.assertIn('_auth_user_id', self.client.session)

    def test_logout(self):
        self.client.login(username=self.admin_username, password=self.admin_password)
        response = self.client.post(reverse('accounts/logout/'))

        # chech that the user is redirected to LOGOUT_REDIRECT_URL
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('sobaka:all_humans'))  
        response = self.client.get(reverse('admin:index'))  
        self.assertRedirects(response, reverse('/accounts/login/')) 

        self.assertNotIn('_auth_user_id', self.client.session) 


class SignUpTestCase(TestCase):
    def setUp(self):
        self.signup_url = reverse('signup')
        
    def test_signup_page_status_code(self):
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200) 

    def test_signup_form_valid(self):
        # Test that creates new user and redirects to the 'all_humans' page
        
        data = {
            'username': 'testadmin',
            'password1': 'testpassword',
            'password2': 'testpassword', 
            'email': 'testadmin@test.com'
        }
        
        response = self.client.post(self.signup_url, data)

        # user is redirected test
        self.assertRedirects(response, reverse('sobaka:all_humans'))  

        user = User.objects.get(username='testuser')
        self.assertEqual(user.email, 'testadmin@test.com')

    def test_signup_invalid_email(self):
        #invalid email
        
        data = {
            'username': 'testuser',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'email': 'invalid-email'
        }
        
        response = self.client.post(self.signup_url, data)

        self.assertFormError(response, 'form', 'email', 'Enter a valid email address.')

    def test_signup_wrong_password(self):
        #wrong password
        
        data = {
            'username': 'testuser',
            'password1': 'testpassword',
            'password2': 'differentpassword',
            'email': 'testadmin@test.com'
        }

        response = self.client.post(self.signup_url, data)

        self.assertFormError(response, 'form', 'password2', 'The two password fields didn’t match.')

    def test_invalid_username(self):
        #invalid username test
        
        data = {
            'username': 'newuser!',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'email': 'testadmin@test.com'
        }

        response = self.client.post(self.signup_url, data)
        self.assertFormError(response, 'form', 'username', 'Enter a valid username.')

    def test_signup_redirect_logged_in_user(self):
        self.client.login(username='testadmin', password='testpassword')
        response = self.client.get(self.signup_url)
        self.assertRedirects(response, reverse('sobaka:all_humans'))

class HumanListViewTestCase(TestCase):

    def test_pagination_links(self):
        #first page link
        response = self.client.get(reverse('sobaka:all_humans') + '?page=1')
        self.assertContains(response, 'href="?page=2"')  # There should be a "next" link to the second page

        #second page link
        response = self.client.get(reverse('sobaka:all_humans') + '?page=2')
        self.assertContains(response, 'href="?page=3"')  

        #"previous" link on the second page
        self.assertContains(response, 'href="?page=1"')

