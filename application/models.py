from django.db import models
from django.conf import settings

from datetime import date

from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField


class Person(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True
    )

    given_name_kana = models.CharField(max_length=50, blank=True)
    family_name_kana = models.CharField(max_length=50, blank=True)
    middle_name_kana = models.CharField(max_length=50, blank=True)

    given_name_hanzi = models.CharField(max_length=20, blank=True)
    family_name_hanzi = models.CharField(max_length=20, blank=True)

    MALE = 'M'
    FEMALE = 'F'
    OTHER = 'O'
    GENDER_CHOICES = (
        (MALE, "Male"),
        (FEMALE, "Female"),
        (OTHER, "Other"),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default=OTHER)

    birthdate = models.DateField('date of birth')

    nationality = CountryField()
    present_address = models.TextField(blank=True)
    permanent_address = models.TextField(blank=True)
    mobile_number = PhoneNumberField()
    phone_number = PhoneNumberField(blank=True)
    fax_number = PhoneNumberField(blank=True)

    special = models.TextField(blank=True)

    def __str__(self):
        return "%s (%s)" % (self.user.get_full_name(), self.user.email)

    @property
    def age(self):
        today = date.today()
        born = self.birthdate
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

    @property
    def emergency(self):
        return self.user.emergencycontact_set

    @property
    def workplace(self):
        return self.user.workplace_set

    @property
    def academic(self):
        a = self.user.academicinstitution_set
        r = { s.level: s.details for s in a.all() }
        if a:
            r['total'] = { 'duration': "%.1f" % sum(s.duration for s in a.all()) }
            r['current'] = a.last().details
        return r

    def languages(self):
        langs = { 'JAPANESE': 'j', 'ENGLISH': 'e' }
        for l in self.user.languageproficiency_set.all():
            yield langs.get(l.language.upper(), 'o'), l.details

    @property
    def details(self):
        return {
            'gender': self.gender,
            'birthdate': self.birthdate,
            'nationality': self.nationality.name,
            'special': self.special,
            'age': self.age,
            'emergency': tuple(c.details for c in self.emergency.all()),
            'work': tuple(w.details for w in self.workplace.all()),
            'school': self.academic,
            'language': { k: v for k, v in self.languages() },
        }


class Enrollment(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True
    )

    KUMAMOTO = 'KM'
    YATSUSHIRO = 'YS'
    CAMPUS_CHOICES = (
        (KUMAMOTO, '熊本'),
        (YATSUSHIRO, '八代'),
    )
    campus = models.CharField(max_length=10, choices=CAMPUS_CHOICES, default=KUMAMOTO)

    supervisor = models.OneToOneField(settings.AUTH_USER_MODEL,
            on_delete=models.CASCADE, related_name='+', blank=True, null=True
    )
    department = models.CharField(max_length=50, blank=True)

    start = models.DateField()
    end = models.DateField()

    field_of_study = models.TextField(blank=True)
    study_plans = models.TextField(blank=True)

    def __str__(self):
        return "%s (%s)" % (self.user.get_full_name(), self.user.email)

    @property
    def details(self):
        return {
            'campus': self.campus,
            'field_of_study': self.field_of_study,
            'study_plans': self.study_plans,
            'start': self.start,
            'end': self.end,
        }

class EmergencyContact(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    relation = models.CharField(max_length=50)
    name = models.CharField(max_length=100)

    address = models.TextField(blank=True)
    phone_number = PhoneNumberField()
    fax_number = PhoneNumberField(blank=True)
    email_address = models.EmailField(blank=True)

    def __str__(self):
        return "%s - %s" % (self.user.get_full_name(), self.relation)

    @property
    def details(self):
        return {
            'relation': self.relation,
            'name': self.name,
            'address': self.address,
            'phone_number': self.phone_number,
            'fax_number': self.phone_number,
        }


class AcademicInstitution(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=50)

    start = models.DateField()
    end = models.DateField(blank=True, null=True)

    ISCED_LEVELS = (
        (1, "Elementary"),
        (2, "Secondary"),
        (3, "Upper Secondary"),
        (4, "Post-secondary"),
        (6, "University (Undergraduate)"),
        (7, "University (Master's)"),
        (8, "University (Doctorate)"),
    )

    level = models.PositiveSmallIntegerField(choices=ISCED_LEVELS)
    progress_year = models.PositiveSmallIntegerField()

    def __str__(self):
        return "%s - %s" % (self.user.get_full_name(), self.level)

    @property
    def duration(self):
        ydiff = self.end.year - self.start.year
        mdiff = self.end.month - self.start.month
        return ydiff + (mdiff+1)/12

    @property
    def details(self):
        return {
            'name': self.name,
            'location': self.location,
            'level': self.level,
            'progress': "%d-%d" % (self.level, self.progress_year),
            'start': self.start,
            'end': self.end,
            'duration': "%.1f" % self.duration,
        }

    class Meta:
        ordering = ('level',)


class Workplace(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=50)

    start = models.DateField()
    end = models.DateField(blank=True, null=True)

    def __str__(self):
        return "%s - %s" % (self.user.get_full_name(), self.name)

    @property
    def details(self):
        return {
            'name': self.name,
            'location': self.location,
            'start': self.start,
            'end': self.end,
        }

    class Meta:
        ordering = ('start',)


class LanguageProficiency(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    language = models.CharField(max_length=20)

    SCALE = tuple((i,i) for i in range(1, 6))

    writing = models.PositiveSmallIntegerField(choices=SCALE)
    reading = models.PositiveSmallIntegerField(choices=SCALE)
    speaking = models.PositiveSmallIntegerField(choices=SCALE)
    listening = models.PositiveSmallIntegerField(choices=SCALE)

    def __str__(self):
        return "%s - %s" % (self.user.get_full_name(), self.language)

    @property
    def details(self):
        return {
            'writing': self.writing,
            'reading': self.reading,
            'speaking': self.speaking,
            'listening': self.listening,
            'name': self.language,
        }


class VisaApplication(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True
    )

    passport_number = models.CharField(max_length=20)
    passport_expiry = models.DateField()

    application_place = CountryField()
    entry_port = models.CharField(max_length=50)
    entry_date = models.DateField()
    stay_days = models.PositiveSmallIntegerField()

    past_entries = models.PositiveSmallIntegerField()
    last_entry = models.DateField(null=True, blank=True)
    last_exit = models.DateField(null=True, blank=True)

    def __str__(self):
        return "%s (%s)" % (self.user.get_full_name(), self.user.email)

    @property
    def details(self):
        ent = bool(self.past_entries)
        return {
            'passport_number': self.passport_number,
            'passport_expiry': self.passport_expiry,
            'application_place': self.application_place,
            'entry_port': self.entry_port,
            'entry_date': self.entry_date,
            'stay_days': "%d days" % self.stay_days,
            'past_entrance': ent,
            'past_entries': self.past_entries if ent else '',
            'last_entry': self.last_entry if ent else '',
            'last_exit': self.last_exit if ent else '',
        }
