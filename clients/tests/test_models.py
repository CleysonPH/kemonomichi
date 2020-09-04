from datetime import date

from django.test import TestCase
from django.urls import reverse

from clients.models import Address, Client


class AddressModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """"Set up non-modified object used by all test methods"""
        Address.objects.create(
            street="Rua Altos",
            city="Teresina",
            state="PI",
        )

    def test_street_label(self):
        address = Address.objects.get(pk=1)
        street_label = address._meta.get_field("street").verbose_name
        self.assertEqual(street_label, "Rua")

    def test_street_max_length(self):
        address = Address.objects.get(pk=1)
        max_length = address._meta.get_field("street").max_length
        self.assertEqual(max_length, 50)

    def test_city_label(self):
        address = Address.objects.get(pk=1)
        city_label = address._meta.get_field("city").verbose_name
        self.assertEqual(city_label, "Cidade")

    def test_city_max_length(self):
        address = Address.objects.get(pk=1)
        max_length = address._meta.get_field("city").max_length
        self.assertEqual(max_length, 30)

    def test_state_label(self):
        address = Address.objects.get(pk=1)
        state_label = address._meta.get_field("state").verbose_name
        self.assertEqual(state_label, "Estado")

    def test_state_max_length(self):
        address = Address.objects.get(pk=1)
        max_length = address._meta.get_field("state").max_length
        self.assertEqual(max_length, 2)

    def test_string_representation(self):
        address = Address.objects.get(pk=1)
        self.assertEqual(
            str(address), f"{address.street}, {address.city} - {address.state}"
        )

    def test_verbose_name(self):
        verbose_name = Address._meta.verbose_name
        self.assertEqual(str(verbose_name), "endereço")

    def test_verbose_name_plural(self):
        verbose_name_plural = Address._meta.verbose_name_plural
        self.assertEqual(str(verbose_name_plural), "endereços")


class ClientModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """"Set up non-modified object used by all test methods"""
        address = Address.objects.create(
            street="Rua Altos",
            city="Teresina",
            state="PI",
        )
        Client.objects.create(
            name="José Augusto",
            email="jose@mail.com",
            address=address,
            cpf="123.456.789-12",
            birth_date=date(1990, 1, 1),
            occupation="Pessoa Desenvolvedora",
        )

    def test_name_label(self):
        client = Client.objects.get(pk=1)
        name_label = client._meta.get_field("name").verbose_name
        self.assertEqual(name_label, "Nome")

    def test_name_max_length(self):
        client = Client.objects.get(pk=1)
        max_length = client._meta.get_field("name").max_length
        self.assertEqual(max_length, 100)

    def test_email_label(self):
        client = Client.objects.get(pk=1)
        email_label = client._meta.get_field("email").verbose_name
        self.assertEqual(email_label, "Email")

    def test_address_label(self):
        client = Client.objects.get(pk=1)
        address_label = client._meta.get_field("address").verbose_name
        self.assertEqual(address_label, "Endereço")

    def test_cpf_label(self):
        client = Client.objects.get(pk=1)
        cpf_label = client._meta.get_field("cpf").verbose_name
        self.assertEqual(cpf_label, "CPF")

    def test_cpf_max_length(self):
        client = Client.objects.get(pk=1)
        max_length = client._meta.get_field("cpf").max_length
        self.assertEqual(max_length, 14)

    def test_birth_date_label(self):
        client = Client.objects.get(pk=1)
        birth_date_label = client._meta.get_field("birth_date").verbose_name
        self.assertEqual(birth_date_label, "Data de Nascimento")

    def test_occupation_label(self):
        client = Client.objects.get(pk=1)
        occupation_label = client._meta.get_field("occupation").verbose_name
        self.assertEqual(occupation_label, "Profissão")

    def test_occupation_max_length(self):
        client = Client.objects.get(pk=1)
        max_length = client._meta.get_field("occupation").max_length
        self.assertEqual(max_length, 25)

    def test_string_representation(self):
        client = Client.objects.get(pk=1)
        self.assertEqual(str(client), client.name)

    def test_verbose_name(self):
        verbose_name = Client._meta.verbose_name
        self.assertEqual(str(verbose_name), "cliente")

    def test_verbose_name_plural(self):
        verbose_name_plural = Client._meta.verbose_name_plural
        self.assertEqual(str(verbose_name_plural), "clientes")

    def test_get_absolute_url(self):
        client = Client.objects.get(pk=1)
        self.assertEqual(
            client.get_absolute_url(),
            reverse("clients:client-detail", args=[client.pk]),
        )
