# Generated by Django 5.1.3 on 2024-12-01 00:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Jogador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('pontos', models.IntegerField(default=0)),
                ('data', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]