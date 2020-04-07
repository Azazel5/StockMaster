from django.db import models

class CompanyModel(models.Model):
    company_name = models.CharField(max_length=255)

class CompanyStockInformation(models.Model):
    company = models.ForeignKey(CompanyModel, on_delete=models.CASCADE)
    number_of_transactions = models.IntegerField()
    maximum = models.FloatField()
    minimum = models.FloatField()
    closing = models.FloatField()
    traded_shares = models.FloatField()
    amount = models.FloatField()
    previous_closing = models.FloatField()
    difference_rs = models.FloatField()

    class Meta:
        verbose_name_plural = 'Company stock information'