from datetime import date

from django.test import TestCase
from django.urls import reverse
from model_bakery import baker

from pets.models import Pet
from employees.models import Employee


class PetCreateViewTest(TestCase):
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
        self.owner = baker.make("clients.Client")

    def test_view_url_exists_at_desired_location(self):
        self.client.login(**self.admin_credentials)
        response = self.client.get(f"/pets/cadastrar/{self.owner.pk}/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(**self.admin_credentials)
        response = self.client.get(reverse("pets:pet-create", args=[self.owner.pk]))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(**self.admin_credentials)
        response = self.client.get(reverse("pets:pet-create", args=[self.owner.pk]))
        self.assertTemplateUsed(response, "pets/pet_form.html")

    def test_page_title(self):
        self.client.login(**self.admin_credentials)
        response = self.client.get(reverse("pets:pet-create", args=[self.owner.pk]))
        self.assertIn("title", response.context)
        self.assertEqual(response.context["title"], "Cadastrar Pet")

    def test_redirects_to_pet_detail_after_submit_form_with_success(self):
        self.client.login(**self.admin_credentials)
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
        self.client.login(**self.admin_credentials)
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

    def test_redirect_to_signin_when_not_authenticated(self):
        url = reverse("pets:pet-create", args=[self.owner.pk])
        response = self.client.get(url)
        self.assertRedirects(response, (reverse("accounts:signin") + f"?next={url}"))


class PetDetailViewTest(TestCase):
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
        self.pet = baker.make(Pet)

    def test_view_url_exists_at_desired_location(self):
        self.client.login(**self.admin_credentials)
        response = self.client.get(f"/pets/{self.pet.pk}/detalhes/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(**self.admin_credentials)
        response = self.client.get(reverse("pets:pet-detail", args=[self.pet.pk]))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(**self.admin_credentials)
        response = self.client.get(reverse("pets:pet-detail", args=[self.pet.pk]))
        self.assertTemplateUsed(response, "pets/pet_detail.html")

    def test_page_title(self):
        self.client.login(**self.admin_credentials)
        response = self.client.get(reverse("pets:pet-detail", args=[self.pet.pk]))
        self.assertIn("title", response.context)
        self.assertEqual(response.context["title"], "Detalhes do Pet")

    def test_show_correct_pet(self):
        self.client.login(**self.admin_credentials)
        response = self.client.get(reverse("pets:pet-detail", args=[self.pet.pk]))
        self.assertIn("pet", response.context)
        self.assertEqual(response.context["pet"], self.pet)

    def test_redirect_to_signin_when_not_authenticated(self):
        url = reverse("pets:pet-detail", args=[self.pet.pk])
        response = self.client.get(url)
        self.assertRedirects(response, (reverse("accounts:signin") + f"?next={url}"))


class PetDeleteViewTest(TestCase):
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
        self.pet_data = baker.make("pets.Pet")

    def test_view_url_exists_at_desired_location(self):
        self.client.login(**self.admin_credentials)
        response = self.client.get(f"/pets/{self.pet_data.pk}/remover/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(**self.admin_credentials)
        response = self.client.get(reverse("pets:pet-delete", args=[self.pet_data.pk]))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(**self.admin_credentials)
        response = self.client.get(reverse("pets:pet-delete", args=[self.pet_data.pk]))
        self.assertTemplateUsed(response, "pets/pet_delete_confirm.html")

    def test_page_title(self):
        self.client.login(**self.admin_credentials)
        response = self.client.get(reverse("pets:pet-delete", args=[self.pet_data.pk]))
        self.assertIn("title", response.context)
        self.assertEqual(response.context["title"], "Remover Pet")

    def test_show_correct_pet(self):
        self.client.login(**self.admin_credentials)
        response = self.client.get(reverse("pets:pet-delete", args=[self.pet_data.pk]))
        self.assertIn("pet", response.context)
        self.assertEqual(response.context["pet"], self.pet_data)

    def test_redirects_to_pet_detail_after_submit_form_with_success(self):
        self.client.login(**self.admin_credentials)
        response = self.client.post(reverse("pets:pet-delete", args=[self.pet_data.pk]))

        self.assertRedirects(response, reverse("clients:client-detail", args=[1]))

    def test_delete_pet_in_database_after_submit_form_with_success(self):
        self.client.login(**self.admin_credentials)
        response = self.client.post(
            reverse("pets:pet-delete", args=[self.pet_data.pk]),
        )

        with self.assertRaises(Pet.DoesNotExist):
            Pet.objects.get(pk=1)

    def test_redirect_to_signin_when_not_authenticated(self):
        url = reverse("pets:pet-delete", args=[self.pet_data.pk])
        response = self.client.get(url)
        self.assertRedirects(response, (reverse("accounts:signin") + f"?next={url}"))


class PetUpdateViewTest(TestCase):
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
        self.pet_data = baker.make("pets.Pet")

    def test_view_url_exists_at_desired_location(self):
        self.client.login(**self.admin_credentials)
        response = self.client.get(f"/pets/{self.pet_data.pk}/atualizar/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(**self.admin_credentials)
        response = self.client.get(reverse("pets:pet-update", args=[self.pet_data.pk]))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(**self.admin_credentials)
        response = self.client.get(reverse("pets:pet-update", args=[self.pet_data.pk]))
        self.assertTemplateUsed(response, "pets/pet_form.html")

    def test_page_title(self):
        self.client.login(**self.admin_credentials)
        response = self.client.get(reverse("pets:pet-update", args=[self.pet_data.pk]))
        self.assertIn("title", response.context)
        self.assertEqual(response.context["title"], "Editar Pet")

    def test_show_correct_pet(self):
        self.client.login(**self.admin_credentials)
        response = self.client.get(reverse("pets:pet-update", args=[self.pet_data.pk]))
        self.assertIn("pet_form", response.context)
        self.assertEqual(
            response.context["pet_form"].instance,
            self.pet_data,
        )

    def test_redirects_to_pet_detail_after_submit_form_with_success(self):
        self.client.login(**self.admin_credentials)
        response = self.client.post(
            reverse("pets:pet-update", args=[self.pet_data.pk]),
            {
                "name": "Mimi",
                "birth_date": date(1990, 12, 30),
                "specie": "GA",
                "color": "BR",
            },
        )

        self.assertRedirects(
            response, reverse("pets:pet-detail", args=[self.pet_data.pk])
        )

    def test_update_pet_in_database_after_submit_form_with_success(self):
        self.client.login(**self.admin_credentials)
        pet_data = {
            "name": "Mimi",
            "birth_date": date(1990, 12, 30),
            "specie": "GA",
            "color": "BR",
        }

        response = self.client.post(
            reverse("pets:pet-update", args=[self.pet_data.pk]),
            pet_data,
        )

        pet = Pet.objects.get(pk=self.pet_data.pk)

        self.assertEqual(pet_data["name"], pet.name)
        self.assertEqual(pet_data["birth_date"], pet.birth_date)
        self.assertEqual(pet_data["specie"], pet.specie)
        self.assertEqual(pet_data["color"], pet.color)

    def test_redirect_to_signin_when_not_authenticated(self):
        url = reverse("pets:pet-update", args=[self.pet_data.pk])
        response = self.client.get(url)
        self.assertRedirects(response, (reverse("accounts:signin") + f"?next={url}"))