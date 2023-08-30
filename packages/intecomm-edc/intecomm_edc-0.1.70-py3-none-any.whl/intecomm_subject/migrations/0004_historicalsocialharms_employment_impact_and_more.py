# Generated by Django 4.1.2 on 2022-12-02 23:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("intecomm_subject", "0003_alter_historicalsocialharms_coworkers_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="historicalsocialharms",
            name="employment_impact",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="NOT_APPLICABLE",
                max_length=25,
                verbose_name="... with your partner?",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="historicalsocialharms",
            name="employment_impact_help",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="N/A",
                max_length=25,
                verbose_name="Would you like help",
            ),
        ),
        migrations.AddField(
            model_name="historicalsocialharms",
            name="employment_impact_referal",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="N/A",
                max_length=25,
                verbose_name="Has the participant been referred for further help",
            ),
        ),
        migrations.AddField(
            model_name="historicalsocialharms",
            name="employment_impact_severity",
            field=models.CharField(
                choices=[
                    ("minor", "Minor"),
                    ("moderate", "Moderate"),
                    ("major", "Major"),
                    ("N/A", "Not applicable"),
                ],
                default="N/A",
                max_length=25,
                verbose_name="Severity of impact",
            ),
        ),
        migrations.AddField(
            model_name="historicalsocialharms",
            name="employment_impact_status",
            field=models.CharField(
                choices=[
                    ("resolved", "Resolved"),
                    ("ongoing", "Ongoing"),
                    ("N/A", "Not applicable"),
                ],
                default="N/A",
                max_length=25,
                verbose_name="Status of impact",
            ),
        ),
        migrations.AddField(
            model_name="historicalsocialharms",
            name="healthcare_impact",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="NOT_APPLICABLE",
                max_length=25,
                verbose_name="... with your partner?",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="historicalsocialharms",
            name="healthcare_impact_help",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="N/A",
                max_length=25,
                verbose_name="Would you like help",
            ),
        ),
        migrations.AddField(
            model_name="historicalsocialharms",
            name="healthcare_impact_referal",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="N/A",
                max_length=25,
                verbose_name="Has the participant been referred for further help",
            ),
        ),
        migrations.AddField(
            model_name="historicalsocialharms",
            name="healthcare_impact_severity",
            field=models.CharField(
                choices=[
                    ("minor", "Minor"),
                    ("moderate", "Moderate"),
                    ("major", "Major"),
                    ("N/A", "Not applicable"),
                ],
                default="N/A",
                max_length=25,
                verbose_name="Severity of impact",
            ),
        ),
        migrations.AddField(
            model_name="historicalsocialharms",
            name="healthcare_impact_status",
            field=models.CharField(
                choices=[
                    ("resolved", "Resolved"),
                    ("ongoing", "Ongoing"),
                    ("N/A", "Not applicable"),
                ],
                default="N/A",
                max_length=25,
                verbose_name="Status of impact",
            ),
        ),
        migrations.AddField(
            model_name="historicalsocialharms",
            name="insurance_impact",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="NOT_APPLICABLE",
                max_length=25,
                verbose_name="... with your partner?",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="historicalsocialharms",
            name="insurance_impact_help",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="N/A",
                max_length=25,
                verbose_name="Would you like help",
            ),
        ),
        migrations.AddField(
            model_name="historicalsocialharms",
            name="insurance_impact_referal",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="N/A",
                max_length=25,
                verbose_name="Has the participant been referred for further help",
            ),
        ),
        migrations.AddField(
            model_name="historicalsocialharms",
            name="insurance_impact_severity",
            field=models.CharField(
                choices=[
                    ("minor", "Minor"),
                    ("moderate", "Moderate"),
                    ("major", "Major"),
                    ("N/A", "Not applicable"),
                ],
                default="N/A",
                max_length=25,
                verbose_name="Severity of impact",
            ),
        ),
        migrations.AddField(
            model_name="historicalsocialharms",
            name="insurance_impact_status",
            field=models.CharField(
                choices=[
                    ("resolved", "Resolved"),
                    ("ongoing", "Ongoing"),
                    ("N/A", "Not applicable"),
                ],
                default="N/A",
                max_length=25,
                verbose_name="Status of impact",
            ),
        ),
        migrations.AddField(
            model_name="historicalsocialharms",
            name="other_impact",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="NOT_APPLICABLE",
                max_length=25,
                verbose_name="... with your partner?",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="historicalsocialharms",
            name="other_impact_description",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="historicalsocialharms",
            name="other_impact_help",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="N/A",
                max_length=25,
                verbose_name="Would you like help",
            ),
        ),
        migrations.AddField(
            model_name="historicalsocialharms",
            name="other_impact_referal",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="N/A",
                max_length=25,
                verbose_name="Has the participant been referred for further help",
            ),
        ),
        migrations.AddField(
            model_name="historicalsocialharms",
            name="other_impact_severity",
            field=models.CharField(
                choices=[
                    ("minor", "Minor"),
                    ("moderate", "Moderate"),
                    ("major", "Major"),
                    ("N/A", "Not applicable"),
                ],
                default="N/A",
                max_length=25,
                verbose_name="Severity of impact",
            ),
        ),
        migrations.AddField(
            model_name="historicalsocialharms",
            name="other_impact_status",
            field=models.CharField(
                choices=[
                    ("resolved", "Resolved"),
                    ("ongoing", "Ongoing"),
                    ("N/A", "Not applicable"),
                ],
                default="N/A",
                max_length=25,
                verbose_name="Status of impact",
            ),
        ),
        migrations.AddField(
            model_name="historicalsocialharms",
            name="other_service_impact",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="NOT_APPLICABLE",
                max_length=25,
                verbose_name="... with your partner?",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="historicalsocialharms",
            name="other_service_impact_description",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="historicalsocialharms",
            name="other_service_impact_help",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="N/A",
                max_length=25,
                verbose_name="Would you like help",
            ),
        ),
        migrations.AddField(
            model_name="historicalsocialharms",
            name="other_service_impact_referal",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="N/A",
                max_length=25,
                verbose_name="Has the participant been referred for further help",
            ),
        ),
        migrations.AddField(
            model_name="historicalsocialharms",
            name="other_service_impact_severity",
            field=models.CharField(
                choices=[
                    ("minor", "Minor"),
                    ("moderate", "Moderate"),
                    ("major", "Major"),
                    ("N/A", "Not applicable"),
                ],
                default="N/A",
                max_length=25,
                verbose_name="Severity of impact",
            ),
        ),
        migrations.AddField(
            model_name="historicalsocialharms",
            name="other_service_impact_status",
            field=models.CharField(
                choices=[
                    ("resolved", "Resolved"),
                    ("ongoing", "Ongoing"),
                    ("N/A", "Not applicable"),
                ],
                default="N/A",
                max_length=25,
                verbose_name="Status of impact",
            ),
        ),
        migrations.AddField(
            model_name="socialharms",
            name="employment_impact",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="NOT_APPLICABLE",
                max_length=25,
                verbose_name="... with your partner?",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="socialharms",
            name="employment_impact_help",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="N/A",
                max_length=25,
                verbose_name="Would you like help",
            ),
        ),
        migrations.AddField(
            model_name="socialharms",
            name="employment_impact_referal",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="N/A",
                max_length=25,
                verbose_name="Has the participant been referred for further help",
            ),
        ),
        migrations.AddField(
            model_name="socialharms",
            name="employment_impact_severity",
            field=models.CharField(
                choices=[
                    ("minor", "Minor"),
                    ("moderate", "Moderate"),
                    ("major", "Major"),
                    ("N/A", "Not applicable"),
                ],
                default="N/A",
                max_length=25,
                verbose_name="Severity of impact",
            ),
        ),
        migrations.AddField(
            model_name="socialharms",
            name="employment_impact_status",
            field=models.CharField(
                choices=[
                    ("resolved", "Resolved"),
                    ("ongoing", "Ongoing"),
                    ("N/A", "Not applicable"),
                ],
                default="N/A",
                max_length=25,
                verbose_name="Status of impact",
            ),
        ),
        migrations.AddField(
            model_name="socialharms",
            name="healthcare_impact",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="NOT_APPLICABLE",
                max_length=25,
                verbose_name="... with your partner?",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="socialharms",
            name="healthcare_impact_help",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="N/A",
                max_length=25,
                verbose_name="Would you like help",
            ),
        ),
        migrations.AddField(
            model_name="socialharms",
            name="healthcare_impact_referal",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="N/A",
                max_length=25,
                verbose_name="Has the participant been referred for further help",
            ),
        ),
        migrations.AddField(
            model_name="socialharms",
            name="healthcare_impact_severity",
            field=models.CharField(
                choices=[
                    ("minor", "Minor"),
                    ("moderate", "Moderate"),
                    ("major", "Major"),
                    ("N/A", "Not applicable"),
                ],
                default="N/A",
                max_length=25,
                verbose_name="Severity of impact",
            ),
        ),
        migrations.AddField(
            model_name="socialharms",
            name="healthcare_impact_status",
            field=models.CharField(
                choices=[
                    ("resolved", "Resolved"),
                    ("ongoing", "Ongoing"),
                    ("N/A", "Not applicable"),
                ],
                default="N/A",
                max_length=25,
                verbose_name="Status of impact",
            ),
        ),
        migrations.AddField(
            model_name="socialharms",
            name="insurance_impact",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="NOT_APPLICABLE",
                max_length=25,
                verbose_name="... with your partner?",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="socialharms",
            name="insurance_impact_help",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="N/A",
                max_length=25,
                verbose_name="Would you like help",
            ),
        ),
        migrations.AddField(
            model_name="socialharms",
            name="insurance_impact_referal",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="N/A",
                max_length=25,
                verbose_name="Has the participant been referred for further help",
            ),
        ),
        migrations.AddField(
            model_name="socialharms",
            name="insurance_impact_severity",
            field=models.CharField(
                choices=[
                    ("minor", "Minor"),
                    ("moderate", "Moderate"),
                    ("major", "Major"),
                    ("N/A", "Not applicable"),
                ],
                default="N/A",
                max_length=25,
                verbose_name="Severity of impact",
            ),
        ),
        migrations.AddField(
            model_name="socialharms",
            name="insurance_impact_status",
            field=models.CharField(
                choices=[
                    ("resolved", "Resolved"),
                    ("ongoing", "Ongoing"),
                    ("N/A", "Not applicable"),
                ],
                default="N/A",
                max_length=25,
                verbose_name="Status of impact",
            ),
        ),
        migrations.AddField(
            model_name="socialharms",
            name="other_impact",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="NOT_APPLICABLE",
                max_length=25,
                verbose_name="... with your partner?",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="socialharms",
            name="other_impact_description",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="socialharms",
            name="other_impact_help",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="N/A",
                max_length=25,
                verbose_name="Would you like help",
            ),
        ),
        migrations.AddField(
            model_name="socialharms",
            name="other_impact_referal",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="N/A",
                max_length=25,
                verbose_name="Has the participant been referred for further help",
            ),
        ),
        migrations.AddField(
            model_name="socialharms",
            name="other_impact_severity",
            field=models.CharField(
                choices=[
                    ("minor", "Minor"),
                    ("moderate", "Moderate"),
                    ("major", "Major"),
                    ("N/A", "Not applicable"),
                ],
                default="N/A",
                max_length=25,
                verbose_name="Severity of impact",
            ),
        ),
        migrations.AddField(
            model_name="socialharms",
            name="other_impact_status",
            field=models.CharField(
                choices=[
                    ("resolved", "Resolved"),
                    ("ongoing", "Ongoing"),
                    ("N/A", "Not applicable"),
                ],
                default="N/A",
                max_length=25,
                verbose_name="Status of impact",
            ),
        ),
        migrations.AddField(
            model_name="socialharms",
            name="other_service_impact",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="NOT_APPLICABLE",
                max_length=25,
                verbose_name="... with your partner?",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="socialharms",
            name="other_service_impact_description",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name="socialharms",
            name="other_service_impact_help",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="N/A",
                max_length=25,
                verbose_name="Would you like help",
            ),
        ),
        migrations.AddField(
            model_name="socialharms",
            name="other_service_impact_referal",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                default="N/A",
                max_length=25,
                verbose_name="Has the participant been referred for further help",
            ),
        ),
        migrations.AddField(
            model_name="socialharms",
            name="other_service_impact_severity",
            field=models.CharField(
                choices=[
                    ("minor", "Minor"),
                    ("moderate", "Moderate"),
                    ("major", "Major"),
                    ("N/A", "Not applicable"),
                ],
                default="N/A",
                max_length=25,
                verbose_name="Severity of impact",
            ),
        ),
        migrations.AddField(
            model_name="socialharms",
            name="other_service_impact_status",
            field=models.CharField(
                choices=[
                    ("resolved", "Resolved"),
                    ("ongoing", "Ongoing"),
                    ("N/A", "Not applicable"),
                ],
                default="N/A",
                max_length=25,
                verbose_name="Status of impact",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsocialharms",
            name="coworkers_impact",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                max_length=25,
                verbose_name="... with your partner?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsocialharms",
            name="family_impact",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                max_length=25,
                verbose_name="... with your partner?",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsocialharms",
            name="friends_impact",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                max_length=25,
                verbose_name="... with your partner?",
            ),
        ),
        migrations.AlterField(
            model_name="socialharms",
            name="coworkers_impact",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                max_length=25,
                verbose_name="... with your partner?",
            ),
        ),
        migrations.AlterField(
            model_name="socialharms",
            name="family_impact",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                max_length=25,
                verbose_name="... with your partner?",
            ),
        ),
        migrations.AlterField(
            model_name="socialharms",
            name="friends_impact",
            field=models.CharField(
                choices=[("Yes", "Yes"), ("No", "No"), ("N/A", "Not applicable")],
                max_length=25,
                verbose_name="... with your partner?",
            ),
        ),
    ]
