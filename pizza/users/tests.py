import django.test

import users.models
import cart.models


class UserTests(django.test.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        client = django.test.Client()

        cls.address = users.models.Address.objects.create(
            address="Нахабино, ул.Панфилова, д9, кв199"
        )

        cls.address.save()

    def test_create_user_success(self):
        data = [{
            "name": "user",
            "surname": "user_surname",
            "phone": "+79266701107",
            "email": "testmail@gmail.com",
            "tg_token": "@abobus",
            "password": "Password19",
        }, {
            "email": "mail@gmail.com",
            "password": "Password191"
        }]
        for i in data:
            count_users = users.models.User.objects.count()
            count_carts = cart.models.Cart.objects.count()
            user = users.models.User.objects.create_user(**i)

            user.addresses.set([self.address])
            user.save()
            self.assertEqual(count_users + 1, users.models.User.objects.count())
            self.assertEqual(count_carts + 1, cart.models.Cart.objects.count())
            self.assertEqual(user.username, user.email)

    def test_create_super_user(self):
        count_users = users.models.User.objects.count()
        count_carts = cart.models.Cart.objects.count()
        data = {
            "name": "user",
            "surname": "user_surname",
            "phone": "+79266701107",
            "email": "testmail@gmail.com",
            "tg_token": "@abobus",
            "password": "Password19",
        }

        user = users.models.User.objects.create_superuser(**data)

        user.addresses.set([self.address])
        user.save()
        self.assertEqual(count_users + 1, users.models.User.objects.count())
        self.assertEqual(count_carts + 1, cart.models.Cart.objects.count())
        self.assertEqual(user.email, user.username)
