from django.db import models
from django.conf import settings

class Farmer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='farmer_profile')
    farmer_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, unique=True)
    H_start_date = models.DateField()
    location = models.CharField(max_length=255)
    fpo_name = models.CharField(max_length=100)
    rice_type = models.CharField(max_length=50)
    water_source = models.CharField(max_length=100)
    staff = models.ForeignKey('Staff', on_delete=models.CASCADE, related_name='farmer_profile')
    geoJSON = models.JSONField() 

    def __str__(self):
        return self.farmer_name


class Staff(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='staff_profile')
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, unique=True)
    location = models.CharField(max_length=255)
    fpo_name = models.CharField(max_length=100) 

    def __str__(self):
        return self.name

class AnalysesTable(models.Model):
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='analyses')
    ndvi = models.FloatField(help_text="Normalized Difference Vegetation Index")
    rendvi = models.FloatField(help_text="Red Edge Normalized Difference Vegetation Index")
    ndmi = models.FloatField(help_text="Normalized Difference Moisture Index")
    ndwi = models.FloatField(help_text="Normalized Difference Water Index")
    ci = models.FloatField(help_text="Chlorophyll Index")
    analysis_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Analysis'
        verbose_name_plural = 'Analyses'
        ordering = ['-analysis_date']

    def __str__(self):
        return f"Analysis for {self.farmer.name} on {self.analysis_date}"

    def calculate_report(self):
        """
        Method to generate a report based on analysis values.
        Can include any logic to generate the PDF report.
        """
        # Report generation logic can be added here
        pass