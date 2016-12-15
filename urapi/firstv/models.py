from __future__ import unicode_literals

from django.db import models

# Create your models here.
class FeedBack(models.Model):
	sellerName = models.CharField(max_length=50)
	isTopRated = models.CharField(max_length=30)
	fstmonthPostive = models.IntegerField()
	fstmonthNetural = models.IntegerField()
	fstMonthNegative = models.IntegerField()
	sixMonthPostive = models.IntegerField()
	sixMonthNetural = models.IntegerField()
	sixMonthNegative = models.IntegerField()
	tweMonthPostive = models.IntegerField()
	tweMonthNetural = models.IntegerField()
	tweMonthNegative = models.IntegerField()
	createdDate = models.DateTimeField()

class ebayAccount(models.Model):
	sellerName = models.CharField(max_length=50)
