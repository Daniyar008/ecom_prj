# Generated migration for fixing User.bio field

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("userauths", "0007_alter_profile_address_alter_profile_country_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="bio",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
