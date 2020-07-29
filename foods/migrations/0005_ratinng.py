# Generated by Django 3.0.8 on 2020-07-31 23:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('foods', '0004_auto_20200729_0317'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ratinng',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(default=0)),
                ('food_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foods.Food')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
