# Generated by Django 5.0 on 2024-10-16 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0002_alter_student_first_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='first_name',
            field=models.CharField(max_length=200),
        ),
    ]
