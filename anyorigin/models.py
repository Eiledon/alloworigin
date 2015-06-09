from django.db import models

class Request(models.Model):
    ip = models.GenericIPAddressField()
    dest = models.URLField()

    def __str__(self):
        return self.dest