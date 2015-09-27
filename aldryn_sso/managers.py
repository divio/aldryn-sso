# -*- coding: utf-8 -*-
from django.db.models import Manager


class AldrynCloudUserManager(Manager):

    def get_queryset(self):
        return super(AldrynCloudUserManager, self).get_queryset().select_related('user')
