from django.db import models
from django.utils import timezone


class CompanyModel(models.Model):
    company_name = models.CharField(max_length=255)

    def __str__(self):
        return self.company_name

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
    date_added = models.DateField(default=timezone.now)

    def __str__(self):
        return self.company.company_name + ' | ' + str(self.date_added)

    class Meta:
        verbose_name_plural = 'Company stock information'