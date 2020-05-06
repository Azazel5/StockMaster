from django.db import models


class ModelCompany(models.Model):
# Model for static company information, which will enever change.

    company_symbol = models.CharField(max_length=100)
    company_name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.company_name


class ModelDynamicInfo(models.Model):
#  One more company model for information like latest cash dividends, etc
#  Find more stuff which may be useful here 

    company = models.ForeignKey(ModelCompany, on_delete=models.CASCADE)
    latest_bonus_share = models.CharField(max_length=100)
    latest_cash_dividend = models.CharField(max_length=100)
    year = models.DateField(auto_now=False, auto_now_add=False)
    book_close_date = models.DateField(auto_now=False, auto_now_add=False)

    def __str__(self):
        return f'{self.company.company_name} with {self.latest_bonus_share}'

class ModelStock(models.Model):
    company = models.ForeignKey(ModelCompany, on_delete=models.CASCADE)
    conf = models.FloatField()
    open_price = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    vwap = models.FloatField()
    volume = models.FloatField()
    prev_close = models.FloatField()
    turnover= models.FloatField()

    trans = models.FloatField()
    difference_rs = models.FloatField()
    range_rs = models.FloatField()
    difference_percent = models.FloatField()
    range_percent = models.FloatField()
    vwap_percent = models.FloatField()
    oneeighty_days = models.FloatField()
    fiftytwo_week_high = models.FloatField()
    fiftytwo_week_low = models.FloatField()

    date_added = models.DateField(auto_now=False, auto_now_add=False)

    def __str__(self):
        return self.company.company_name + ' | ' + str(self.date_added)

    class Meta:
        verbose_name_plural = 'Company stock information'




