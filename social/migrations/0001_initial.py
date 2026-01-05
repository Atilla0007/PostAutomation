from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SocialAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('platform', models.CharField(choices=[('instagram', 'Instagram'), ('facebook', 'Facebook'), ('tiktok', 'TikTok'), ('youtube', 'YouTube'), ('linkedin', 'LinkedIn'), ('x', 'X')], max_length=20)),
                ('display_name', models.CharField(max_length=255)),
                ('account_type', models.CharField(blank=True, choices=[('instagram_professional', 'Instagram Professional'), ('instagram_personal', 'Instagram Personal'), ('facebook_page', 'Facebook Page'), ('facebook_profile', 'Facebook Profile')], max_length=64)),
                ('permissions_valid', models.BooleanField(default=False)),
                ('tiktok_photo_post_enabled', models.BooleanField(default=False)),
                ('tiktok_prerequisites_met', models.BooleanField(default=False)),
                ('linkedin_access_granted', models.BooleanField(default=False)),
                ('x_media_upload_enabled', models.BooleanField(default=False)),
                ('x_api_tier', models.CharField(blank=True, max_length=64)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
