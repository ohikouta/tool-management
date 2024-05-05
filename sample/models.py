from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    birth_date = models.DateField(null=True, blank=True)
    # 他に必要なフィールドがあれば追加します


class SWOT(models.Model):
    title = models.CharField(max_length=100)

class SwotIdeas(models.Model):
    swot = models.ForeignKey(SWOT, on_delete=models.CASCADE)
    category_choices = (
        ('Strength', 'Strength'),
        ('Weakness', "Weakness"),
        ('Opportunity', 'Opportunity'),
        ('Threat', 'Threat'),
    )
    category = models.CharField(max_length=20, choices=category_choices)
    content = models.CharField(max_length=300)

