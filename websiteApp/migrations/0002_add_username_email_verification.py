# Generated manually for username and email verification

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


def populate_usernames(apps, schema_editor):
    """Populate username field for existing users based on email"""
    CustomUser = apps.get_model('websiteApp', 'CustomUser')
    for user in CustomUser.objects.all():
        if not user.username:
            # Generate username from email
            base_username = user.email.split('@')[0]
            username = base_username
            counter = 1
            # Ensure uniqueness
            while CustomUser.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1
            user.username = username
            user.save()


def mark_existing_users_verified(apps, schema_editor):
    """Mark existing users as verified since they were created before verification was required"""
    CustomUser = apps.get_model('websiteApp', 'CustomUser')
    CustomUser.objects.all().update(email_verified=True)


class Migration(migrations.Migration):

    dependencies = [
        ('websiteApp', '0001_initial'),
    ]

    operations = [
        # Add username as nullable first
        migrations.AddField(
            model_name='customuser',
            name='username',
            field=models.CharField(max_length=150, null=True, unique=True, blank=True),
        ),
        # Populate usernames for existing users
        migrations.RunPython(populate_usernames, migrations.RunPython.noop),
        # Make username non-nullable
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(max_length=150, unique=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='email_verified',
            field=models.BooleanField(default=False),
        ),
        # Mark existing users as verified
        migrations.RunPython(mark_existing_users_verified, migrations.RunPython.noop),
        migrations.CreateModel(
            name='EmailVerificationToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=64, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('expires_at', models.DateTimeField()),
                ('is_used', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='verification_tokens', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

