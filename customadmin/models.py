# customadmin/models.py 
from django.db import models

class VCFFile(models.Model):
    name = models.CharField(max_length=100, unique=True)
    max_contacts = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
  
class Contact(models.Model):
    vcf_file = models.ForeignKey(VCFFile, on_delete=models.CASCADE, related_name='contacts')
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)

    class Meta:
        unique_together = ('vcf_file', 'phone')

    def __str__(self):
        return f"{self.name} ({self.phone})"