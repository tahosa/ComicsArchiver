from django.db import models

# Create your models here.
class Comic(models.Model):
    name = models.TextField(unique=True)
    description = models.TextField()
    folder = models.TextField()
    next_regex = models.TextField()
    comic_regex = models.TextField()
    notes_regex = models.TextField()
    alt_text = models.IntegerField(default=0)
    base_url = models.TextField()
    start_url = models.TextField()
    last_url = models.TextField()
    active = models.IntegerField(default=1)

    def __str__(self):
        return self.name

class File(models.Model):
    comic = models.ForeignKey(Comic)
    num = models.IntegerField(null=False)
    filename = models.TextField(null=False)
    alt_text = models.TextField()
    annotation = models.TextField()

    class Meta:
        unique_together = (('comic', 'num'), ('comic', 'filename'))

    def __str__(self):
        return self.filename
