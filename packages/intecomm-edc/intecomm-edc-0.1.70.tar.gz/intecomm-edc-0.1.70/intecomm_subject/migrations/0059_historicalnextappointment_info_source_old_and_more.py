# Generated by Django 4.2.3 on 2023-07-25 17:32

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("edc_visit_schedule", "0010_alter_subjectschedulehistory_options_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("sites", "0002_alter_domain_unique"),
        ("edc_next_appointment", "0001_initial"),
        (
            "intecomm_subject",
            "0058_rename_external_remittance_currency_healtheconomicsincome_external_remit_currency_and_more",
        ),
    ]

    operations = [
        migrations.RenameField(
            model_name="historicalnextappointment",
            old_name="info_source",
            new_name="info_source_old",
        ),
        migrations.AddField(
            model_name="historicalnextappointment",
            name="visitschedule",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                help_text="Click SAVE to let the EDC suggest. Once selected, interim appointments will be flagged as not required/missed.",
                max_length=15,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="edc_visit_schedule.visitschedule",
                verbose_name="Which study visit code is closest to this appointment date",
            ),
        ),
        migrations.RenameField(
            model_name="nextappointment",
            old_name="info_source",
            new_name="info_source_old",
        ),
        migrations.AddField(
            model_name="nextappointment",
            name="visitschedule",
            field=models.ForeignKey(
                help_text="Click SAVE to let the EDC suggest. Once selected, interim appointments will be flagged as not required/missed.",
                max_length=15,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="edc_visit_schedule.visitschedule",
                verbose_name="Which study visit code is closest to this appointment date",
            ),
        ),
        migrations.AlterField(
            model_name="historicalnextappointment",
            name="best_visit_code",
            field=models.CharField(
                help_text="Click SAVE to let the EDC suggest. Once selected, interim appointments will be flagged as not required/missed.",
                max_length=15,
                null=True,
                verbose_name="Which study visit code is closest to this appointment date",
            ),
        ),
        migrations.AlterField(
            model_name="nextappointment",
            name="best_visit_code",
            field=models.CharField(
                help_text="Click SAVE to let the EDC suggest. Once selected, interim appointments will be flagged as not required/missed.",
                max_length=15,
                null=True,
                verbose_name="Which study visit code is closest to this appointment date",
            ),
        ),
    ]
