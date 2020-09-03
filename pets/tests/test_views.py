from datetime import date

from django.test import TestCase
from django.urls import reverse
from model_mommy import mommy

from pets.models import Pet


class PetCreateViewTest(TestCase):
    def setUp(self):
        self.owner = mommy.make("clients.Client")

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(f"/pets/cadastrar/{self.owner.pk}/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("pets:pet-create", args=[self.owner.pk]))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("pets:pet-create", args=[self.owner.pk]))
        self.assertTemplateUsed(response, "pets/pet_form.html")

    def test_page_title(self):
        response = self.client.get(reverse("pets:pet-create", args=[self.owner.pk]))
        self.assertIn("title", response.context)
        self.assertEqual(response.context["title"], "Cadastrar Pet")

    def test_redirects_to_pet_detail_after_submit_form_with_success(self):
        response = self.client.post(
            reverse("pets:pet-create", args=[self.owner.pk]),
            {
                "name": "Tutucão",
                "birth_date": date(2018, 11, 20),
                "specie": "CA",
                "color": "MA",
            },
        )

        self.assertRedirects(response, reverse("pets:pet-detail", args=[1]))

    def test_create_pet_in_database_after_submit_form_with_success(self):
        pet_data = {
            "name": "Tutucão",
            "birth_date": date(2018, 11, 20),
            "specie": "CA",
            "color": "MA",
        }
        response = self.client.post(
            reverse("pets:pet-create", args=[self.owner.pk]),
            pet_data,
        )

        pet = Pet.objects.get(name="Tutucão")

        self.assertEqual(pet_data["name"], pet.name)
        self.assertEqual(pet_data["birth_date"], pet.birth_date)
        self.assertEqual(pet_data["specie"], pet.specie)
        self.assertEqual(pet_data["color"], pet.color)