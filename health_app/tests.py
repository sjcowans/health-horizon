from django.test import TestCase
from .models import UserProfile, DateInfo
from datetime import date

### Model tests ###

class UserProfileModelTests(TestCase):

    def test_user_creation(self):
        user = UserProfile.objects.create_user(
            username='testuser',
            password='testpass123',
            age=25,
            sex='M',
            height=175
        )
        self.assertIsInstance(user, UserProfile)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertEqual(user.username, 'testuser')

    def test_superuser_creation(self):
        user = UserProfile.objects.create_superuser(
            username='admin',
            password='adminpass123',
            age=30,
            sex='F',
            height=165
        )
        self.assertIsInstance(user, UserProfile)
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

class DateInfoModelTests(TestCase):

    def setUp(self):
        self.user = UserProfile.objects.create_user(
            username='testuser',
            password='testpass123',
            age=25,
            sex='M',
            height=175
        )

    def test_dateinfo_creation(self):
        date_info = DateInfo.objects.create(
            user=self.user,
            sleep=480,
            calories=2200,
            stress=20,
            steps=5000,
            weight=65,
            wellness_score=85
        )
        self.assertIsInstance(date_info, DateInfo)
        self.assertEqual(date_info.date, date.today())

from django.test import TestCase
from .forms import UserProfileCreationForm

### Form Tests ###

class UserProfileCreationFormTests(TestCase):

    def test_valid_form(self):
        data = {
            'username': 'newuser',
            'password1': 'newpass123',
            'password2': 'newpass123',
            'age': 30,
            'sex': 'F',
            'height': 160
        }
        form = UserProfileCreationForm(data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.username, 'newuser')
        self.assertTrue(user.check_password('newpass123'))

    def test_invalid_password_confirmation(self):
        data = {
            'username': 'newuser',
            'password1': 'newpass123',
            'password2': 'wrongpass123',
            'age': 30,
            'sex': 'F',
            'height': 160
        }
        form = UserProfileCreationForm(data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
from django.test import TestCase, Client
from django.urls import reverse
from health_app.models import UserProfile, DateInfo
from health_app.forms import UserProfileCreationForm

class UserProfileViewTests(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.user = UserProfile.objects.create_user(username='testuser', password='testpass123', age=25, sex='M', height=175)

    def test_userprofile_list_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('userprofile_list'))
        self.assertEqual(response.status_code, 200)

    def test_userprofile_detail_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('userprofile_detail', args=[self.user.id]))
        self.assertEqual(response.status_code, 200)

    def test_userprofile_create_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('userprofile_create'), {
            'username': 'testuser2',
            'age': 30,
            'sex': 'F',
            'height': 165,
            'password1': 'testpass456',
            'password2': 'testpass456'
        })
        self.assertEqual(response.status_code, 302)  # Assuming a redirect after successful creation.

    def test_userprofile_update_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('userprofile_update', args=[self.user.id]), {
            'username': 'updateduser',
            'age': 26,
            'sex': 'F',
            'height': 180
        })
        self.assertEqual(response.status_code, 302)  # Assuming a redirect after successful update.
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updateduser')

    def test_userprofile_delete_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('userprofile_delete', args=[self.user.id]))
        self.assertEqual(response.status_code, 302)  # Assuming a redirect after successful deletion.
        with self.assertRaises(UserProfile.DoesNotExist):
            self.user.refresh_from_db()

