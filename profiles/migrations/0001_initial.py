import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=200)),
                ('last_name', models.CharField(blank=True, max_length=200)),
                ('bio', models.TextField(blank=True, default='no bio...', max_length=300)),
                ('country', models.CharField(blank=True, max_length=200)),
                ('gender', models.CharField(blank=True, choices=[('male', 'male'), ('female', 'female')], default='male', max_length=6)),
                ('date_of_birth', models.DateField(blank=True, default=datetime.date.today)),
                ('avatar', models.ImageField(default='avatars/avatar.png', upload_to='avatars/')),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('friends', models.ManyToManyField(blank=True, related_name='friends', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Relationship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('send', 'send'), ('accepted', 'accepted')], max_length=8)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to='profiles.Profile')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender', to='profiles.Profile')),
            ],
        ),
    ]
