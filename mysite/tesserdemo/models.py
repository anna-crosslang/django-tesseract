from django.db import models

# Create your models here.

class ReadText(models.Model):
    creation_date = models.DateTimeField('date created')


class Line(models.Model):
    read_text = models.ForeignKey(ReadText, on_delete=models.CASCADE)
    line_text = models.CharField(max_length=400)
    line_number = models.IntegerField(default=0)
