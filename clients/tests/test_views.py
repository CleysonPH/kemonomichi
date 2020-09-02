from datetime import date

from django.test import TestCase
from django.urls import reverse
from model_mommy import mommy

from clients.models import Client


class ClientListViewTest(TestCase):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/clientes/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("clients:client-list"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("clients:client-list"))
        self.assertTemplateUsed(response, "clients/client_list.html")

    def test_page_title(self):
        response = self.client.get(reverse("clients:client-list"))
        self.assertIn("title", response.context)
        self.assertEqual(response.context["title"], "Lista de Clientes")

    def test_list_all_clients(self):
        clients = mommy.make("clients.Client", 10)
        response = self.client.get(reverse("clients:client-list"))
        self.assertEqual(len(response.context["clients"]), 10)

        for client in clients:
            self.assertTrue(client in response.context["clients"])


class ClientDetailViewTest(TestCase):
    def setUp(self):
        """"Set up non-modified object used by all test methods"""
        self.client_data = mommy.make("clients.Client")

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/clientes/1/detalhes/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(
            reverse("clients:client-detail", args=[self.client_data.id])
        )
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(
            reverse("clients:client-detail", args=[self.client_data.id])
        )
        self.assertTemplateUsed(response, "clients/client_detail.html")

    def test_page_title(self):
        response = self.client.get(
            reverse("clients:client-detail", args=[self.client_data.id])
        )
        self.assertIn("title", response.context)
        self.assertEqual(response.context["title"], "Detalhes do Cliente")

    def test_show_correct_client(self):
        response = self.client.get(
            reverse("clients:client-detail", args=[self.client_data.id])
        )
        self.assertIn("client", response.context)
        self.assertEqual(response.context["client"], self.client_data)


class ClientCreateViewTest(TestCase):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/clientes/cadastrar/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("clients:client-create"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("clients:client-create"))
        self.assertTemplateUsed(response, "clients/client_form.html")

    def test_page_title(self):
        response = self.client.get(reverse("clients:client-create"))
        self.assertIn("title", response.context)
        self.assertEqual(response.context["title"], "Cadastrar Cliente")

    def test_redirects_to_client_detail_after_submit_form_with_success(self):
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
        response = self.client.post(
            reverse("clients:client-create"),
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

        client = Client.objects.get(name="Algusto da Silva")

        self.assertRedirects(
            response, reverse("clients:client-detail", args=[client.pk])
        )
        self.assertTrue(client)