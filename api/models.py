from django.db import models

class DeviceUser(models.Model):
    # Kita tidak pakai username/password, tapi pakai ID unik dari HP/Browser
    device_id = models.CharField(max_length=100, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Device {self.device_id}"

class Note(models.Model):
    user = models.ForeignKey(DeviceUser, on_delete=models.CASCADE, related_name='notes')
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    color = models.CharField(max_length=100, default='bg-yellow-100') 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Matkul(models.Model):
    user = models.ForeignKey(DeviceUser, on_delete=models.CASCADE, related_name='matkuls')
    name = models.CharField(max_length=100)
    sks = models.IntegerField()
    grade = models.CharField(max_length=5) # A, B+, dll
    created_at = models.DateTimeField(auto_now_add=True)