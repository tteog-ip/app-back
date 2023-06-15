from django.db import models

class AppStatus(models.Model):
    status = models.CharField(max_length=20)
    class Meta:
        db_table = 'app_status'


class Application(models.Model):
    apt = models.ForeignKey('products.Apt', on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    status = models.ForeignKey(AppStatus, on_delete=models.CASCADE)
    class Meta:
        db_table = 'applications'
