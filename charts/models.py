from django.db import models

# Create your models here.
class Editors(models.Model):
    editor_name = models.CharField(max_length=200)
    num_users = models.IntegerField()

    def __str__(self):
        return "{}-{}".format(self.editor_name, self.num_users) 

class Claims(models.Model):
    billed_amount = models.FloatField()
    allowed_amount = models.FloatField()
    primary_dx = models.CharField(max_length=7)
    claim_ID = models.IntegerField()
    billing_provider_name = models.CharField(max_length=255)
    billing_provider_ID = models.IntegerField()
    claim_type = models.CharField(max_length=255)
    savings_amount = models.FloatField()

class Providers(models.Model):
    provider_id = models.IntegerField()
    provider_name = models.CharField(null=True, max_length=255)
    tax_ID = models.CharField(null=True, max_length=10)
    state = models.CharField(null=True, max_length=2)
    city = models.CharField(null=True, max_length=255)
    zipcode = models.CharField(null=True, max_length=7)
