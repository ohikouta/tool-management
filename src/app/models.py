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

class FourPAnalysis(models.Model):
    overview = models.TextField(verbose_name="概要", blank=True)       # 追加例
    memo = models.TextField(verbose_name="プロジェクトメモ", blank=True)  # 追加例
    product = models.TextField(verbose_name="製品")
    price = models.TextField(verbose_name="価格")
    place = models.TextField(verbose_name="流通")
    promotion = models.TextField(verbose_name="販促")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日")

    def __str__(self):
        return f"4P分析 {self.id}"

