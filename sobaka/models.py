from django.db import models
import uuid
from django.urls import reverse
from datetime import date

def upload_to_human(instance, filename):
    return f'human/{instance.name}/{filename}'

class Category(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    name = models.CharField(max_length=250, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='category', blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_absolute_url(self):
        return reverse('sobaka:humans_by_category', args=[self.id])

    def __str__(self):
        return self.name

class UnavailableDate(models.Model):
    human = models.ForeignKey('Human', on_delete=models.CASCADE, related_name='unavailable_dates')
    date = models.DateField()

    def __str__(self):
        return f"{self.human.name} - {self.date}"

class Human(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    name = models.CharField(max_length=250, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image1 = models.ImageField(upload_to=upload_to_human, blank=True)
    image2 = models.ImageField(upload_to=upload_to_human, blank=True)
    image3 = models.ImageField(upload_to=upload_to_human, blank=True)
    image4 = models.ImageField(upload_to=upload_to_human, blank=True)
    image5 = models.ImageField(upload_to=upload_to_human, blank=True)
    available = models.BooleanField(default=True)
    height = models.IntegerField(blank=True, null=True)
    shoe_size = models.IntegerField(blank=True, null=True)
    waist_size = models.IntegerField(blank=True, null=True)
    bust_size = models.IntegerField(blank=True, null=True)
    hip_size = models.IntegerField(blank=True, null=True)
    eye_color = models.CharField(max_length=250, blank=True)
    hair_color = models.CharField(max_length=250, blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'human'
        verbose_name_plural = 'humans'

    def get_absolute_url(self):
        return reverse('sobaka:human_detail', args=[self.category.id, self.id])

    def is_available_on(self, booking_date):
        return not self.unavailable_dates.filter(date=booking_date).exists()

    def __str__(self):
        return self.name

class Review(models.Model):
    human = models.ForeignKey(Human, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # Rating from 1 to 5
    comment = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f"Review for {self.human.name} by {self.user.username}"

class NewsArticle(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    title = models.CharField(max_length=250, unique=True)
    image = models.ImageField(upload_to='news', blank=True)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created']
        verbose_name = 'news article'
        verbose_name_plural = 'news articles'

    def __str__(self):
        return self.title