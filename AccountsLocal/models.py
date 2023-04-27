from django.db import models
import shortuuid

# Create your models here.
class UserLocal(models.Model):
    id = models.CharField(primary_key=True, editable=False, max_length=10)
    name = models.CharField(max_length=256)
    email = models.EmailField(max_length=254)
    def __str__(self):
        return self.id
    def save(self, *args, **kwargs):
        if len(self.id)==0:
            self.id = shortuuid.uuid()[:10]
        super(UserLocal, self).save(*args, **kwargs)