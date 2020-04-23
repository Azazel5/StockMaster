from django.db import models

"""
    Model for static company information, which will enever change.
"""
class ModelCompany(models.Model):
    company_name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.company_name

"""
    One more company model for information like latest cash dividends, etc
    All scraped from searching on the website
"""



