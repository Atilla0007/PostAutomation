from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('social', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_type', models.CharField(choices=[('TEXT', 'Text'), ('PHOTO', 'Photo'), ('VIDEO', 'Video')], max_length=10)),
                ('caption', models.TextField(blank=True)),
                ('hashtags', models.JSONField(blank=True, default=list)),
                ('image_file', models.FileField(blank=True, null=True, upload_to='images/')),
                ('video_file', models.FileField(blank=True, null=True, upload_to='videos/')),
                ('media_metadata', models.JSONField(blank=True, default=dict)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PostTarget',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('selected', 'Selected'), ('queued', 'Queued'), ('rejected', 'Rejected'), ('published', 'Published')], default='selected', max_length=10)),
                ('last_error', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='targets', to='posts.post')),
                ('social_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='social.socialaccount')),
            ],
            options={
                'unique_together': {('post', 'social_account')},
            },
        ),
    ]
