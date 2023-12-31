# Generated by Django 4.2.5 on 2023-09-26 12:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("watchlist_app", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="StreamPlatform",
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
                ("name", models.CharField(max_length=30)),
                ("about", models.CharField(max_length=200)),
                ("website", models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name="WatchList",
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
                ("title", models.CharField(max_length=50)),
                ("storyline", models.CharField(max_length=200)),
                ("active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "platform",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="watchlist",
                        to="watchlist_app.streamplatform",
                    ),
                ),
            ],
        ),
        migrations.DeleteModel(
            name="Movie",
        ),
    ]
