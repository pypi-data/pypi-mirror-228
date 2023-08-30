# Generated by Django 4.1.2 on 2022-11-21 18:17

import django.contrib.sites.models
from django.db import migrations, models
import django.db.models.deletion
import django_crypto_fields.fields.encrypted_char_field


class Migration(migrations.Migration):
    dependencies = [
        ("sites", "0002_alter_domain_unique"),
        (
            "intecomm_screening",
            "0002_remove_healthtalklog_unique_lower_name_report_date_and_more",
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="Site",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("sites.site",),
            managers=[
                ("objects", django.contrib.sites.models.SiteManager()),
            ],
        ),
        migrations.RemoveField(
            model_name="historicalpatientlog",
            name="patient_group",
        ),
        migrations.RemoveField(
            model_name="patientlog",
            name="patient_group",
        ),
        migrations.AlterField(
            model_name="historicalpatientlog",
            name="hf_identifier",
            field=django_crypto_fields.fields.encrypted_char_field.EncryptedCharField(
                blank=True,
                db_index=True,
                help_text="Must be unique (Encryption: RSA local)",
                max_length=71,
                verbose_name="Health center identifier",
            ),
        ),
        migrations.AlterField(
            model_name="patientlog",
            name="hf_identifier",
            field=django_crypto_fields.fields.encrypted_char_field.EncryptedCharField(
                blank=True,
                help_text="Must be unique (Encryption: RSA local)",
                max_length=71,
                unique=True,
                verbose_name="Health center identifier",
            ),
        ),
        migrations.AlterField(
            model_name="historicalpatientlog",
            name="site",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="intecomm_screening.site",
                verbose_name="Health center",
            ),
        ),
        migrations.AlterField(
            model_name="patientlog",
            name="site",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="+",
                to="intecomm_screening.site",
                verbose_name="Health center",
            ),
        ),
    ]
