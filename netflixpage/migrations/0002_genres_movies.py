# Generated by Django 4.2 on 2023-06-18 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("netflixpage", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Genres",
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
                ("genreid", models.IntegerField(max_length=100)),
                ("genre", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Movies",
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
                ("title", models.CharField(max_length=300)),
                ("genres", models.TextField(max_length=300)),
                ("overview", models.TextField(max_length=300)),
                ("releasedate", models.DateTimeField()),
                ("rating", models.IntegerField(default=0)),
                ("posterpath", models.TextField(max_length=300)),
                ("cast", models.TextField(max_length=300, null=True)),
                ("duration", models.IntegerField(default=100, null=True)),
                ("descriptiveadjectives", models.TextField(max_length=300, null=True)),
            ],
        ),
    ]
