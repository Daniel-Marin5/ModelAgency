from django.db import models
import uuid
from django.urls import reverse

class Category(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    name = models.CharField(max_length=250, unique=True)
    description = models.TextField(blank = True)
    image = models.ImageField(upload_to = 'category', blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_absolute_url(self):
        return reverse('sobaka:humans_by_category', args=[self.id])

    def __str__(self):
        return self.name

class Human(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    name = models.CharField(max_length=250, unique=True)
    description = models.TextField(blank = True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to = 'human', blank=True)
    available = models.BooleanField(default=True)
    height = models.DecimalField(max_digits=5, decimal_places=2, blank = True, null= True)
    shoe_size = models.DecimalField(max_digits=5, decimal_places=2, blank = True, null= True)
    waist_size = models.DecimalField(max_digits=5, decimal_places=2, blank = True, null= True)
    bust_size = models.DecimalField(max_digits=5, decimal_places=2, blank = True, null= True)   
    hip_size = models.DecimalField(max_digits=5, decimal_places=2, blank = True, null= True)
    eye_color = models.CharField(max_length=250, blank = True)
    hair_color = models.CharField(max_length=250, blank = True)


    class Meta:
        ordering = ('name',)
        verbose_name = 'human'
        verbose_name_plural = 'humans'

    def get_absolute_url(self):
        return reverse('sobaka:human_detail', args=[self.category.id, self.id])

    def __str__(self):
        return self.name