from http.client import responses
from django.contrib.auth import get_user
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class RegistrationTestCase(TestCase):
    def test_user_account_is_created(self):
        self.client.post(
            reverse("users:register"),
            data={
                "username": "Joxa",
                "first_name": "Jakhon",
                "last_name": "Khudoyberdiyev",
                "email": "xudoyberdiyev8@gmail.com",
                "password": "salompassword"
            }
        )

        user = User.objects.get(username="Joxa")

        self.assertEqual(user.first_name, "Jakhon")
        self.assertEqual(user.last_name, "Khudoyberdiyev")
        self.assertEqual(user.email, "xudoyberdiyev8@gmail.com")
        self.assertNotEqual(user.password, "salompassword")
        self.assertTrue(user.check_password("salompassword"))


    def test_requared_fields(self):
        response = self.client.post(
            reverse("users:register"),
            data={
                "first_name": "Jakhon",
                "email": "xudoyberdiyev8@gmail.com"

            }
        )

        user_count = User.objects.count()


        self.assertEqual(user_count, 0)
        self.assertFormError(response.context['form'],  'username', 'This field is required.')

    def test_invalid_email(self):
        response = self.client.post(
            reverse("users:register"),
            data={
                "username": "Joxa",
                "first_name": "Jakhon",
                "last_name": "Khudoyberdiyev",
                "email": "xudoyberdiyev8@gmail.com",
                "password": "salompassword"
            }
        )

        user_count = User.objects.count()
        self.assertEqual(user_count, 1)

        self.assertFormError(response.context['form'],  'email', 'Enter a valid email address.')

    def test_unique_username(self):
        user = User.objects.create_user(username = "joxa", first_name = "Jaxon")
        user.set_password("somepass")
        user.save()

        response = self.client.post(
            reverse("users:register"),
            data={
                "username": "Joxa",
                "first_name": "Jakhon",
                "last_name": "Khudoyberdiyev",
                "email": "xudoyberdiyev8@gmail.com",
                "password": "salompassword"
            }
        )




class LoginTestCase(TestCase):
    def SetUp(self):
        self.db_user = User.objects.create_user(username="joxa", first_name="Jakhon")
        self.db_user.set_password("somepass")
        self.db_user.save()

    def test_successful_login(self):


        self.client.post(
            reverse("users:login"),
            data = {
                "username": "joxa",
                "password": "<somepass"
            }
        )

        user = get_user(self.client)
        self.assertTrue(user.is_authenticated)

    def test_wrong_credentials(self):

        self.client.post(
            reverse("users:login"),
            data={
                "username": "wrong_user",
                "password": "<somepass"
            }
        )


        user = get_user(self.client)

        self.assertFalse(user.is_authenticated)
    def test_logout(self):

        self.client.login(username="joxa", password="somepass")
        self.client.get(reverse('users:logout'))
        user = get_user(self.client)

        self.assertFalse(user.is_authenticated)


class ProfileTestCase(TestCase):
    def test_login_required(self):
        response = self.client.get(reverse("users:profile"))

        self.assertEqual(response.url, reverse("users:login") + "?next=/users/Profile/")
        self.assertEqual(response.status_code, 302)


    def test_profile_details(self):
        user = User.objects.create_user(username="joxa", first_name="Jaxon", last_name="Khudoyberdiyev", email="xudoyberdiyev8@gmail.com")
        user.set_password("<PASSWORD>")
        user.save()

        self.client.login(username="joxa", password="<PASSWORD>")
        response = self.client.get(reverse("users:profile"))

        self.assertContains(response, user.username)
        self.assertContains(response, user.first_name)
        self.assertContains(response, user.last_name)
        self.assertContains(response, user.email)

        self.assertEqual(response.status_code, 200)





