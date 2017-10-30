from django.db import models
from django.core import validators
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField


CREDIT_SCORE_VALIDATORS = [
    validators.MinValueValidator(300),
    validators.MaxValueValidator(850),
]


class CreationInfo(models.Model):
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True


class ChangingInfo(CreationInfo):
    changed_at = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True


class Organization(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'


class Offer(ChangingInfo):
    CATEGORIES = (
        ('C', 'потреб'),      # consumer credit
        ('M', 'ипотека'),     # mortgage
        ('A', 'автокредит'),  # auto loan
        ('S', 'КМСБ'),        # SME finance
    )

    started_rotating_at = models.DateTimeField()
    ended_rotating_at = models.DateTimeField()
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=1, choices=CATEGORIES)
    min_score = models.IntegerField(
        validators=CREDIT_SCORE_VALIDATORS
    )
    max_score = models.IntegerField(
        validators=CREDIT_SCORE_VALIDATORS
    )
    organization = models.ForeignKey(Organization)

    class Meta:
        verbose_name = 'Предложение'
        verbose_name_plural = 'Предложения'


class CustomerProfile(ChangingInfo):

    first_name = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    birth_day = models.DateField()
    phone = PhoneNumberField()
    passport_number = models.CharField(max_length=10)
    score = models.IntegerField(
        validators=CREDIT_SCORE_VALIDATORS,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Анкета клиента'
        verbose_name_plural = 'Анкеты клиентов'


class Application(CreationInfo):
    STATUSES = (
        (False, 'NEW'),
        (True, 'SENT'),
    )

    sent_at = models.DateTimeField(default=timezone.now)
    customer_profile = models.ForeignKey(CustomerProfile)
    offer = models.ForeignKey(Offer)
    status = models.BooleanField(choices=STATUSES, default=False)

    class Meta:
        verbose_name = 'Заявка в кредитную организацию'
        verbose_name_plural = 'Заявки в кредитные организации'
