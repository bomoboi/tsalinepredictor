from django.db import models

class Airport(models.Model):
    iata_code = models.CharField("the IATA code of the airport", max_length=3,primary_key=True)
    icao_code = models.CharField("the ICAO code of the airport", max_length=4)
    ap_name = models.CharField("the name of the airport", max_length=72)

    def __str__(self):
        return f"{self.iata_code}/{self.icao_code}: {self.ap_name}"

class Record(models.Model):
    date = models.DateTimeField("The date and time of the record")
    pax = models.PositiveSmallIntegerField("the number of passengers given by the record")
    ap = models.ForeignKey(Airport, on_delete=models.CASCADE, verbose_name="the airport the record belongs to")
    checkpoint = models.CharField("the name of the checkpoint in the record", max_length=64)

    def __str__(self):
        return f"{self.date.__str__()}, {self.ap.__str__()}, {self.checkpoint}, {self.pax:,}"
