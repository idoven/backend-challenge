# Generated by Django 3.2.23 on 2024-01-29 22:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('connector', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ecgmodel',
            name='user',
            field=models.ForeignKey(
                default=1,
                help_text='The user who created the ECG',
                on_delete=django.db.models.deletion.CASCADE,
                related_name='ecgs',
                to='connector.usermodel',
            ),
            preserve_default=False,
        ),
    ]
