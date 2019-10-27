# Generated by Django 2.2.6 on 2019-10-05 01:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0007_msgs'),
    ]

    operations = [
        migrations.CreateModel(
            name='answer_views',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('views', models.PositiveIntegerField(default=0)),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.answer')),
                ('user', models.ManyToManyField(related_name='Visitor', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]