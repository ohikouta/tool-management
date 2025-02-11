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



# 2025/02/05追加
class SWOTAnalysis(models.Model):
    """SWOT分析のメタ情報を管理"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class SWOTItem(models.Model):
    """SWOTの各要素（強み、弱み、機会、脅威）を個別管理"""
    CATEGORY_CHOICES = [
        ('Strength', 'Strength'),
        ('Weakness', 'Weakness'),
        ('Opportunity', 'Opportunity'),
        ('Threat', 'Threat'),
    ]
    
    analysis = models.ForeignKey(SWOTAnalysis, on_delete=models.CASCADE, related_name="items")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category}: {self.content[:30]}..."
