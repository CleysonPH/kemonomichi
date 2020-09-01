from django.test import TestCase

from clients.models import Address


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
        self.assertEquals(street_label, "Rua")

    def test_street_max_length(self):
        address = Address.objects.get(pk=1)
        max_length = address._meta.get_field("street").max_length
        self.assertEquals(max_length, 50)

    def test_city_label(self):
        address = Address.objects.get(pk=1)
        city_label = address._meta.get_field("city").verbose_name
        self.assertEquals(city_label, "Cidade")

    def test_city_max_length(self):
        address = Address.objects.get(pk=1)
        max_length = address._meta.get_field("city").max_length
        self.assertEquals(max_length, 30)

    def test_state_label(self):
        address = Address.objects.get(pk=1)
        state_label = address._meta.get_field("state").verbose_name
        self.assertEquals(state_label, "Estado")

    def test_state_max_length(self):
        address = Address.objects.get(pk=1)
        max_length = address._meta.get_field("state").max_length
        self.assertEquals(max_length, 2)

    def test_string_representation(self):
        address = Address.objects.get(pk=1)
        self.assertEquals(
            str(address), f"{address.street}, {address.city} - {address.state}"
        )

    def test_verbose_name(self):
        verbose_name = Address._meta.verbose_name
        self.assertEquals(str(verbose_name), "endereço")

    def test_verbose_name_plural(self):
        verbose_name = Address._meta.verbose_name_plural
        self.assertEquals(str(verbose_name), "endereços")
