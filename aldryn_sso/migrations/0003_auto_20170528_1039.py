from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aldryn_sso', '0002_auto_20161019_1953'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aldrynclouduser',
            name='cloud_id',
            field=models.PositiveIntegerField(unique=True, verbose_name='Cloud ID'),
        ),
        migrations.AlterField(
            model_name='aldrynclouduser',
            name='user',
            field=models.OneToOneField(
                related_name='aldryn_cloud_account',
                verbose_name='User',
                to=settings.AUTH_USER_MODEL,
                on_delete=models.CASCADE,
            ),
        ),
    ]
