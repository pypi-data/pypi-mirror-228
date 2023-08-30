# Generated by Django 4.2.3 on 2023-07-26 13:25

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("intecomm_lists", "0006_consentrefusalreasons_screeningrefusalreasons_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("sites", "0002_alter_domain_unique"),
        ("intecomm_facility", "0002_auto_20230726_2030"),
        (
            "intecomm_screening",
            "0047_rename_historicalhealthfacility_historicaloldhealthfacility_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="healthtalklog",
            name="old_health_facility",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="historicalhealthtalklog",
            name="old_health_facility",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="idenfifierformat",
            name="old_health_facility",
            field=models.CharField(max_length=100, null=True),
        ),
    ]
