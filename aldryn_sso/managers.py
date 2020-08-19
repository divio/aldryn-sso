from django.db.models import Manager


class AldrynCloudUserManager(Manager):

    def get_queryset(self):
        return super().get_queryset().select_related('user')
