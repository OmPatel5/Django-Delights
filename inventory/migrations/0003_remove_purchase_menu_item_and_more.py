# Generated by Django 4.2.3 on 2023-07-09 19:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_reciperequirement_delete_reciperequirements_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchase',
            name='menu_item',
        ),
        migrations.RemoveField(
            model_name='reciperequirement',
            name='ingredient',
        ),
        migrations.DeleteModel(
            name='MenuItem',
        ),
        migrations.DeleteModel(
            name='Purchase',
        ),
        migrations.DeleteModel(
            name='RecipeRequirement',
        ),
    ]
