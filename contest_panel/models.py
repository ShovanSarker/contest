from django.db import models

# Create your models here.


class ContestPanel(models.Model):
    ContestName = models.CharField(max_length=24, null=True, blank=True)
    ContestImage = models.FileField('contest_image', upload_to='images/contest', blank=True, null=True)
    Active = models.BooleanField(default=False)
    NumberOfPhotos = models.IntegerField(default=0)
    DateAdded = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        return self.ContestName


class ContestImage(models.Model):
    Contest = models.ForeignKey(ContestPanel, related_name='the name of the contest')
    NameOfTheContestant = models.CharField(max_length=32)
    EmailOfTheContestant = models.EmailField(blank=True, null=True)
    PhoneOfTheContestant = models.CharField(max_length=32, blank=True, null=True)
    FBLinkOfTheContestant = models.CharField(max_length=64, blank=True, null=True)
    ProfessionOfTheContestant = models.CharField(max_length=64, blank=True, null=True)
    InstituteOfTheContestant = models.CharField(max_length=64, blank=True, null=True)
    PhotoOfTheContestant = models.FileField('contestant_image', upload_to='images/contestant', blank=True, null=True)
    CaptionOfThePhoto = models.TextField()
    DateAdded = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        return self.NameOfTheContestant
