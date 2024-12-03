from django.db import models

class CarBrand(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Region(models.Model):
    objects = models.Manager()
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class QueryType(models.Model):
    objects = models.Manager()
    query_template = models.CharField(max_length=200)

    def __str__(self):
        return self.query_template

class QueryResult(models.Model):
    objects = models.Manager()
    car_brand = models.ForeignKey(CarBrand, on_delete=models.CASCADE)
    region = models.CharField(max_length=200)
    query_text = models.CharField(max_length=200)
    count = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.query_text} ({self.count})"
