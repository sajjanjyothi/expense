# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Expenses(models.Model):
    date = models.DateField('Date')
    travel = models.FloatField('Travel', blank=True,null=True, default=0)
    food = models.FloatField('Food', blank=True,null=True, default=0)
    miscellaneous = models.FloatField('Miscellaneous', blank=True,null=True, default=0)
    total_expense = models.FloatField('Total Expense', blank=True,null=True, default=0)
    descr = models.TextField('Description',max_length=2000,blank=True,null=True, default="")