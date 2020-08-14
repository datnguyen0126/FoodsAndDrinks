from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50)
    parent_id = models.ForeignKey("self", on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.name
