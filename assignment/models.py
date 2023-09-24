from django.db import models

class Projects(models.Model):
    title = models.CharField(max_length=200)
    technologies = models.CharField(max_length=200)
    skillset_frontend = models.CharField(max_length=200)
    skillset_backend = models.CharField(max_length=200)
    skillset_databases = models.CharField(max_length=200)
    skillset_infrastructure = models.CharField(max_length=200)

    class Meta:
            db_table = 'projects'