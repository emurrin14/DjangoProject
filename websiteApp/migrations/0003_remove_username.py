# Generated manually to remove username field

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('websiteApp', '0002_add_username_email_verification'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='username',
        ),
    ]

