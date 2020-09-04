from datetime import date

from django.test import TestCase
from django.urls import reverse
from model_mommy import mommy

from clients.models import Client
from employees.models import Employee


class ClientListViewTest(TestCase):
    def setUp(self):
        self.admin_credentials = {
            "username": "admin_test_username",
            "password": "admin_test_password",
        }
        self.admin_user = Employee.objects.create_user(
            username=self.admin_credentials["username"],
            password=self.admin_credentials["password"],
            email="test@mail.com",
            first_name="Test",
            last_name="User",
            birth_date=date(1990, 1, 1),
            role=1,
        )

    def test_view_url_exists_at_desired_location(self):
        self.client.login(**self.admin_credentials)
        response = self.client.get("/clientes/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(**self.admin_credentials)
        response = self.client.get(reverse("clients:client-list"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(**self.admin_credentials)
        response = self.client.get(reverse("clients:client-list"))
        self.assertTemplateUsed(response, "clients/client_list.html")

    def test_page_title(self):
        self.client.login(**self.admin_credentials)
        response = self.client.get(reverse("clients:client-list"))
        self.assertIn("title", response.context)
        self.assertEqual(response.context["title"], "Lista de Clientes")

    def test_list_all_clients(self):
        self.client.login(**self.admin_credentials)
        clients = mommy.make("clients.Client", 10)
        response = self.client.get(reverse("clients:client-list"))
        self.assertEqual(len(response.context["clients"]), 10)

        for client in clients:
            self.assertTrue(client in response.context["clients"])

    def test_redirect_to_signin_when_not_authenticated(self):
        url = reverse("clients:client-list")
        response = self.client.get(url)
        self.assertRedirects(response, (reverse("accounts:signin") + f"?next={url}"))


class ClientDetailViewTest(TestCase):
    def setUp(self):
        self.admin_credentials = {
            "username": "admin_test_username",
            "password": "admin_test_password",
        }
        self.admin_user = Employee.objects.create_user(
            username=self.admin_credentials["username"],
            password=self.admin_credentials["password"],
            email="test@mail.com",
            first_name="Test",
            last_name="User",
            birth_date=date(1990, 1, 1),
            role=1,
        )
        self.client_data = mommy.make("clients.Client")

    def test_view_url_exists_at_desired_location(self):
        self.client.login(**self.admin_credentials)
        response = self.client.get("/clientes/1/detalhes/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(**self.admin_credentials)
        response = self.client.get(
            reverse("clients:client-detail", args=[self.client_data.id])
        )
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(**self.admin_credentials)
        response = self.client.get(
            reverse("clients:client-detail", args=[self.client_data.id])
        )
        self.assertTemplateUsed(response, "clients/client_detail.html")

    def test_page_title(self):
        self.client.login(**self.admin_credentials)
        response = self.client.get(
            reverse("clients:client-detail", args=[self.client_data.id])
        )
        self.assertIn("title", response.context)
        self.assertEqual(response.context["title"], "Detalhes do Cliente")

    def test_show_correct_client(self):
        self.client.login(**self.admin_credentials)
        response = self.client.get(
            reverse("clients:client-detail", args=[self.client_data.id])
        )
        self.assertIn("client", response.context)
        self.assertEqual(response.context["client"], self.client_data)

    def test_redirect_to_signin_when_not_authenticated(self):
        url = reverse("clients:client-detail", args=[self.client_data.id])
        response = self.client.get(url)
        self.assertRedirects(response, (reverse("accounts:signin") + f"?next={url}"))


class ClientCreateViewTest(TestCase):
    def setUp(self):
        self.admin_credentials = {
            "username": "admin_test_username",
            "password": "admin_test_password",
        }
        self.admin_user = Employee.objects.create_user(
            username=self.admin_credentials["username"],
            password=self.admin_credentials["password"],
            email="test@mail.com",
            first_name="Test",
            last_name="User",
            birth_date=date(1990, 1, 1),
            role=1,
        )

    def test_view_url_exists_at_desired_location(self):
        self.client.login(**self.admin_credentials)
        response = self.client.get("/clientes/cadastrar/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(**self.admin_credentials)
        response = self.client.get(reverse("clients:client-create"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(**self.admin_credentials)
        response = self.client.get(reverse("clients:client-create"))
        self.assertTemplateUsed(response, "clients/client_form.html")

    def test_page_title(self):
        self.client.login(**self.admin_credentials)
        response = self.client.get(reverse("clients:client-create"))
        self.assertIn("title", response.context)
        self.assertEqual(response.context["title"], "Cadastrar Cliente")

    def test_redirects_to_client_detail_after_submit_form_with_success(self):
        self.client.login(**self.admin_credentials)
        response = self.client.post(
            reverse("clients:client-create"),
            {
                "name": "Luis da Silva",
                "email": "luis@mail.com",
                "cpf": "592.362.030-86",
                "birth_date": date(1990, 12, 30),
                "occupation": "Programador",
                "street": "Rua 10",
                "city": "São Paulo",
                "state": "SP",
            },
        )

        self.assertRedirects(response, reverse("clients:client-detail", args=[1]))

    def test_create_client_in_database_after_submit_form_with_success(self):
        self.client.login(**self.admin_credentials)
        client_data = {
            "name": "Algusto da Silva",
            "email": "algusto@mail.com",
            "cpf": "592.362.030-86",
            "birth_date": date(1990, 12, 30),
            "occupation": "Programador",
            "street": "Rua 10",
            "city": "São Paulo",
            "state": "SP",
        }
        response = self.client.post(
            reverse("clients:client-create"),
            client_data,
        )

        client = Client.objects.get(name="Algusto da Silva")

        self.assertRedirects(
            response, reverse("clients:client-detail", args=[client.pk])
        )
        self.assertEqual(client_data["name"], client.name)
        self.assertEqual(client_data["email"], client.email)
        self.assertEqual(client_data["cpf"], client.cpf)
        self.assertEqual(client_data["birth_date"], client.birth_date)
        self.assertEqual(client_data["occupation"], client.occupation)
        self.assertEqual(client_data["street"], client.address.street)
        self.assertEqual(client_data["city"], client.address.city)
        self.assertEqual(client_data["state"], client.address.state)

    def test_redirect_to_signin_when_not_authenticated(self):
        url = reverse("clients:client-create")
        response = self.client.get(url)
        self.assertRedirects(response, (reverse("accounts:signin") + f"?next={url}"))


class ClientUpdateViewTest(TestCase):
    def setUp(self):
        self.admin_credentials = {
            "username": "admin_test_username",
            "password": "admin_test_password",
        }
        self.admin_user = Employee.objects.create_user(
            username=self.admin_credentials["username"],
            password=self.admin_credentials["password"],
            email="test@mail.com",
            first_name="Test",
            last_name="User",
            birth_date=date(1990, 1, 1),
            role=1,
        )
        self.client_data = mommy.make("clients.Client")

    def test_view_url_exists_at_desired_location(self):
        self.client.login(**self.admin_credentials)
        response = self.client.get("/clientes/1/editar/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(**self.admin_credentials)
        response = self.client.get(
            reverse("clients:client-update", args=[self.client_data.pk])
        )
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(**self.admin_credentials)
        response = self.client.get(
            reverse("clients:client-update", args=[self.client_data.pk])
        )
        self.assertTemplateUsed(response, "clients/client_form.html")

    def test_page_title(self):
        self.client.login(**self.admin_credentials)
        response = self.client.get(
            reverse("clients:client-update", args=[self.client_data.pk])
        )
        self.assertIn("title", response.context)
        self.assertEqual(response.context["title"], "Editar Cliente")

    def test_show_correct_client(self):
        self.client.login(**self.admin_credentials)
        response = self.client.get(
            reverse("clients:client-update", args=[self.client_data.pk])
        )
        self.assertIn("client_form", response.context)
        self.assertEqual(
            response.context["client_form"].instance,
            self.client_data,
        )

    def test_redirects_to_client_detail_after_submit_form_with_success(self):
        self.client.login(**self.admin_credentials)
        response = self.client.post(
            reverse("clients:client-update", args=[self.client_data.pk]),
            {
                "name": "Algusto da Silva",
                "email": "algusto@mail.com",
                "cpf": "592.362.030-86",
                "birth_date": date(1990, 12, 30),
                "occupation": "Programador",
                "street": "Rua 10",
                "city": "São Paulo",
                "state": "SP",
            },
        )

        self.assertRedirects(
            response, reverse("clients:client-detail", args=[self.client_data.pk])
        )

    def test_create_client_in_database_after_submit_form_with_success(self):
        self.client.login(**self.admin_credentials)
        client_data = {
            "name": "Algusto da Silva",
            "email": "algusto@mail.com",
            "cpf": "592.362.030-86",
            "birth_date": date(1990, 12, 30),
            "occupation": "Programador",
            "street": "Rua 10",
            "city": "São Paulo",
            "state": "SP",
        }
        response = self.client.post(
            reverse("clients:client-update", args=[self.client_data.pk]),
            client_data,
        )

        client = Client.objects.get(pk=self.client_data.pk)

        self.assertRedirects(
            response, reverse("clients:client-detail", args=[self.client_data.pk])
        )
        self.assertEqual(client_data["name"], client.name)
        self.assertEqual(client_data["email"], client.email)
        self.assertEqual(client_data["cpf"], client.cpf)
        self.assertEqual(client_data["birth_date"], client.birth_date)
        self.assertEqual(client_data["occupation"], client.occupation)
        self.assertEqual(client_data["street"], client.address.street)
        self.assertEqual(client_data["city"], client.address.city)
        self.assertEqual(client_data["state"], client.address.state)

    def test_redirect_to_signin_when_not_authenticated(self):
        url = reverse("clients:client-update", args=[self.client_data.pk])
        response = self.client.get(url)
        self.assertRedirects(response, (reverse("accounts:signin") + f"?next={url}"))


class ClientDeleteViewTest(TestCase):
    def setUp(self):
        self.admin_credentials = {
            "username": "admin_test_username",
            "password": "admin_test_password",
        }
        self.admin_user = Employee.objects.create_user(
            username=self.admin_credentials["username"],
            password=self.admin_credentials["password"],
            email="test@mail.com",
            first_name="Test",
            last_name="User",
            birth_date=date(1990, 1, 1),
            role=1,
        )
        self.client_data = mommy.make("clients.Client")

    def test_view_url_exists_at_desired_location(self):
        self.client.login(**self.admin_credentials)
        response = self.client.get("/clientes/1/remover/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(**self.admin_credentials)
        response = self.client.get(
            reverse("clients:client-delete", args=[self.client_data.pk])
        )
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(**self.admin_credentials)
        response = self.client.get(
            reverse("clients:client-delete", args=[self.client_data.pk])
        )
        self.assertTemplateUsed(response, "clients/client_delete_confirm.html")

    def test_page_title(self):
        self.client.login(**self.admin_credentials)
        response = self.client.get(
            reverse("clients:client-delete", args=[self.client_data.pk])
        )
        self.assertIn("title", response.context)
        self.assertEqual(response.context["title"], "Remover Cliente")

    def test_show_correct_client(self):
        self.client.login(**self.admin_credentials)
        response = self.client.get(
            reverse("clients:client-delete", args=[self.client_data.pk])
        )
        self.assertIn("client", response.context)
        self.assertEqual(response.context["client"], self.client_data)

    def test_redirects_to_client_list_after_submit_form_with_success(self):
        self.client.login(**self.admin_credentials)
        response = self.client.post(
            reverse("clients:client-delete", args=[self.client_data.pk])
        )

        self.assertRedirects(response, reverse("clients:client-list"))

    def test_delete_client_in_database_after_submit_form_with_success(self):
        self.client.login(**self.admin_credentials)
        response = self.client.post(
            reverse("clients:client-delete", args=[self.client_data.pk]),
        )

        self.assertRedirects(response, reverse("clients:client-list"))
        with self.assertRaises(Client.DoesNotExist):
            Client.objects.get(pk=1)

    def test_redirect_to_signin_when_not_authenticated(self):
        url = reverse("clients:client-delete", args=[self.client_data.pk])
        response = self.client.get(url)
        self.assertRedirects(response, (reverse("accounts:signin") + f"?next={url}"))
