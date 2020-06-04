# Generated by Django 3.0.5 on 2020-06-03 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_auto_20200603_1639'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='gender',
        ),
        migrations.AddField(
            model_name='product',
            name='gender',
            field=models.CharField(blank=True, choices=[('none', 'none'), ('man', 'man'), ('woman', 'woman'), ('kids', 'kids')], max_length=30, null=True),
        ),
    ]