from django.test import TestCase
from django.urls import reverse
from .models import Human, Category

# Create your tests here.
class HumanSearchTestCase(TestCase):

    def setUp(self):
        # Create categories
        self.category1 = Category.objects.create(name="Category 1")
        self.category2 = Category.objects.create(name="Category 2")

        # Create humans
        self.human1 = Human.objects.create(
            name="Anna", category=self.category1, price=160.00, available=True,
            height=172, shoe_size=37, bust_size=83, waist_size=60, hip_size=88,
            eye_color="Brown", hair_color="Blonde"
        )
        self.human2 = Human.objects.create(
            name="Diana", category=self.category1, price=130.00, available=True,
            height=178, shoe_size=39, bust_size=76, waist_size=60, hip_size=88,
            eye_color="Brown", hair_color="Brown"
        )
        self.human3 = Human.objects.create(
            name="Edgar", category=self.category2, price=140.00, available=True,
            height=184, shoe_size=43, bust_size=86, waist_size=71, hip_size=90,
            eye_color="Brown", hair_color="Dark Brown"
        )
        self.human4 = Human.objects.create(
            name="Eve", category=self.category1, price=130.00, available=True,
            height=178, shoe_size=39, bust_size=83, waist_size=62, hip_size=90,
            eye_color="Brown", hair_color="Black"
        )
        self.human5 = Human.objects.create(
            name="Goerge", category=self.category2, price=130.00, available=True,
            height=187, shoe_size=44, bust_size=97, waist_size=76, hip_size=96,
            eye_color="Blue", hair_color="Blonde"
        )
        self.human6 = Human.objects.create(
            name="Laura", category=self.category1, price=140.00, available=True,
            height=180, shoe_size=40, bust_size=84, waist_size=60, hip_size=89,
            eye_color="Brown", hair_color="Brown"
        )
        self.human7 = Human.objects.create(
            name="Louis", category=self.category2, price=150.00, available=True,
            height=189, shoe_size=45, bust_size=95, waist_size=80, hip_size=96,
            eye_color="Brown", hair_color="Brown"
        )
        self.human8 = Human.objects.create(
            name="Marco", category=self.category2, price=150.00, available=True,
            height=187, shoe_size=43, bust_size=97, waist_size=76, hip_size=96,
            eye_color="Brown", hair_color="Black"
        )
        self.human9 = Human.objects.create(
            name="Natsya", category=self.category1, price=130.00, available=True,
            height=177, shoe_size=40, bust_size=82, waist_size=59, hip_size=89,
            eye_color="Blue", hair_color="Blonde"
        )
        self.human10 = Human.objects.create(
            name="Nikolas", category=self.category2, price=140.00, available=True,
            height=187, shoe_size=43, bust_size=86, waist_size=69, hip_size=90,
            eye_color="Blue", hair_color="Brown"
        )
        self.human11 = Human.objects.create(
            name="Ray", category=self.category2, price=120.00, available=True,
            height=188, shoe_size=45, bust_size=99, waist_size=79, hip_size=91,
            eye_color="Brown", hair_color="Brown"
        )
        self.human12 = Human.objects.create(
            name="Rosie", category=self.category1, price=120.00, available=True,
            height=179, shoe_size=39, bust_size=80, waist_size=59, hip_size=89,
            eye_color="Blue", hair_color="Ginger"
        )
        self.human13 = Human.objects.create(
            name="Ruth", category=self.category1, price=150.00, available=True,
            height=173, shoe_size=37, bust_size=83, waist_size=60, hip_size=89,
            eye_color="Brown", hair_color="Brown"
        )
        self.human14 = Human.objects.create(
            name="Sara", category=self.category1, price=150.00, available=True,
            height=171, shoe_size=38, bust_size=84, waist_size=60, hip_size=88,
            eye_color="Blue", hair_color="Light Brown"
        )
        self.human15 = Human.objects.create(
            name="Troy", category=self.category2, price=140.00, available=True,
            height=190, shoe_size=45, bust_size=97, waist_size=78, hip_size=94,
            eye_color="Brown", hair_color="Brown"
        )

    def test_search_by_height(self):
        response = self.client.get(reverse('sobaka:all_humans'), {'height': 170})
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.human1, response.context['hums'])
        self.assertNotIn(self.human2, response.context['hums'])

    def test_search_by_shoe_size(self):
        response = self.client.get(reverse('sobaka:all_humans'), {'shoe_size': 42})
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.human2, response.context['hums'])
        self.assertNotIn(self.human1, response.context['hums'])

    def test_search_by_bust_size(self):
        response = self.client.get(reverse('sobaka:all_humans'), {'bust_size': 92})
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.human3, response.context['hums'])
        self.assertNotIn(self.human1, response.context['hums'])

    def test_search_by_waist_size(self):
        response = self.client.get(reverse('sobaka:all_humans'), {'waist_size': 70})
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.human2, response.context['hums'])
        self.assertNotIn(self.human1, response.context['hums'])

    def test_search_by_hip_size(self):
        response = self.client.get(reverse('sobaka:all_humans'), {'hip_size': 90})
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.human1, response.context['hums'])
        self.assertNotIn(self.human2, response.context['hums'])

    def test_search_by_eye_color(self):
        response = self.client.get(reverse('sobaka:all_humans'), {'eye_color': 'Blue'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.human1, response.context['hums'])
        self.assertNotIn(self.human2, response.context['hums'])

    def test_search_by_hair_color(self):
        response = self.client.get(reverse('sobaka:all_humans'), {'hair_color': 'Blonde'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.human1, response.context['hums'])
        self.assertNotIn(self.human2, response.context['hums'])

