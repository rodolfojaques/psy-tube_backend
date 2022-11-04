# Generated by Django 4.1.2 on 2022-11-04 19:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Downloaded",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Video",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("title", models.CharField(max_length=128)),
                ("thumbnail", models.TextField()),
                ("link", models.CharField(max_length=128, unique=True)),
                ("downloads", models.PositiveIntegerField(default=0)),
                (
                    "users",
                    models.ManyToManyField(
                        blank=True,
                        related_name="videos",
                        through="videos.Downloaded",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="downloaded",
            name="video",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="videos.video"
            ),
        ),
    ]
