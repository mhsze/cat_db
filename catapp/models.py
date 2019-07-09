from django.db import models

# Create your models here.
GENDER_CHOICES = (("M", "Male"), ("F", "Female"))


class Home(models.Model):
    HOME_CHOICES = (("LANDED", "Landed"), ("CONDO", "Condominium"))

    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    type = models.CharField(choices=HOME_CHOICES, default="Landed", max_length=100)

    def __str__(self):
        return self.name


class Human(models.Model):
    name = models.CharField(max_length=255)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)
    home = models.ForeignKey(Home, related_name="humans", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Breed(models.Model):
    name = models.CharField(max_length=255)
    origin = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Cat(models.Model):
    name = models.CharField(max_length=255)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)
    breed = models.ForeignKey(Breed, related_name="cats", on_delete=models.CASCADE)
    owner = models.ForeignKey(Human, related_name="cats", on_delete=models.CASCADE)

    def __str__(self):
        return self.name
