from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Department, Employee

class APISampleTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.token_url = reverse('obtain_auth_token')
        self.client.login(username='testuser', password='testpass')
        self.department = Department.objects.create(name='HR', manager='Alice', location='HQ')

    def authenticate(self):
        response = self.client.post(self.token_url, {'username': 'testuser', 'password': 'testpass'})
        token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

    def test_obtain_token(self):
        response = self.client.post(self.token_url, {'username': 'testuser', 'password': 'testpass'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

  

    def test_create_employee(self):
        self.authenticate()
        url = reverse('employee-list')
        data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'phone': '1234567890',
            'department_id': self.department.id,
            'join_date': '2024-01-01',
            'role': 'Engineer',
            'salary': '50000.00'
        }
        response = self.client.post(url, data, format='json')
        print("Response data:", response.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Employee.objects.count(), 1)

    def test_list_employees_requires_auth(self):
        url = reverse('employee-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_employees_authenticated(self):
        self.authenticate()
        url = reverse('employee-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
