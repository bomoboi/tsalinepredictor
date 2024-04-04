from django.db import models

class Airport(models.Model):
    iata_code = models.CharField("the IATA code of the airport", max_length=3,primary_key=True)
    icao_code = models.CharField("the ICAO code of the airport", max_length=4)
    ap_name = models.CharField("the name of the airport", max_length=64)

class Checkpoint():
    checkpoint_name = models.CharField("the name of the checkpoint", max_length=64)
    iata_code = models.ForeignKey(Airport, on_delete=models.CASCADE, verbose_name="the airport the checkpoint is in")

class Record(models.Model):
    date = models.DateField("the date of the record")
    hour = models.PositiveSmallIntegerField("the hour of the record")
    pax = models.PositiveSmallIntegerField("the number of passengers given by the record")
    ap_code = models.ForeignKey(Airport, on_delete=models.CASCADE, verbose_name="the airport the record belongs to")
    checkpoint = models.ForeignKey(Checkpoint, on_delete=models.RESTRICT, verbose_name="the checkpoint of the record")
