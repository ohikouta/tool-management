# Generated by Django 3.2.13 on 2025-02-12 16:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0006_swotanalysis_swotitem'),
    ]

    operations = [
        migrations.CreateModel(
            name='CrossSWOT',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('parent_swot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cross_swot', to='app.swotanalysis')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CrossSWOTItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quadrant', models.CharField(choices=[('Strength', 'Strength'), ('Weakness', 'Weakness'), ('Opportunity', 'Opportunity'), ('Threat', 'Threat')], max_length=20)),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('cross_swot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='app.crossswot')),
            ],
        ),
    ]
