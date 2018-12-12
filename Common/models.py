from django.db import models


class Movie(models.Model):
    m_name = models.CharField(max_length=64)
    m_duration = models.IntegerField(default=90)
    m_leading_role = models.CharField(max_length=128)
    m_director = models.CharField(max_length=64)
    m_open_day = models.DateTimeField(default="1970-1-1 00:00:00")
    m_mode = models.CharField(max_length=32)
    m_price = models.IntegerField(default=0)