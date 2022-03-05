# Generated by Django 4.0.1 on 2022-03-05 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('id', models.UUIDField(editable=False, primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=10)),
                ('time', models.CharField(max_length=20)),
                ('open', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('high', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('low', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('close', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('volume', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('country', models.CharField(max_length=2)),
            ],
        ),
    ]
