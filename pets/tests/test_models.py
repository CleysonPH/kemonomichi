from django.test import TestCase
from django.urls import reverse
from model_mommy import mommy

from pets.models import Pet


class PetModelTest(TestCase):
    def test_name_label(self):
        name_label = Pet._meta.get_field("name").verbose_name
        self.assertEqual(name_label, "Nome")

    def test_name_max_length(self):
        max_length = Pet._meta.get_field("name").max_length
        self.assertEqual(max_length, 50)

    def test_birth_date_label(self):
        birth_date_label = Pet._meta.get_field("birth_date").verbose_name
        self.assertEqual(birth_date_label, "Data de Nascimento")

    def test_specie_label(self):
        specie_label = Pet._meta.get_field("specie").verbose_name
        self.assertEqual(specie_label, "Espécie")

    def test_specie_max_length(self):
        max_length = Pet._meta.get_field("specie").max_length
        self.assertEqual(max_length, 2)

    def test_color_label(self):
        color_label = Pet._meta.get_field("color").verbose_name
        self.assertEqual(color_label, "Cor")

    def test_color_max_length(self):
        max_length = Pet._meta.get_field("color").max_length
        self.assertEqual(max_length, 2)

    def test_owner_label(self):
        owner_label = Pet._meta.get_field("owner").verbose_name
        self.assertEqual(owner_label, "Dono")

    def test_string_representation(self):
        pet = mommy.make(Pet)
        self.assertEqual(str(pet), pet.name)

    def test_verbose_name(self):
        verbose_name = Pet._meta.verbose_name
        self.assertEqual(str(verbose_name), "pet")

    def test_verbose_name_plural(self):
        verbose_name_plural = Pet._meta.verbose_name_plural
        self.assertEqual(str(verbose_name_plural), "pets")

    def test_absolute_url(self):
        pet = mommy.make(Pet)
        self.assertEqual(
            pet.get_absolute_url(), reverse("pets:pet-detail", args=[pet.pk])
        )
