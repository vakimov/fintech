from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core import validators
from django.utils import timezone

from phonenumber_field.modelfields import PhoneNumberField


CREDIT_SCORE_VALIDATORS = [
    validators.MinValueValidator(300),
    validators.MaxValueValidator(850),
]


class User(AbstractUser):
    SUPERUSER = 1
    PARTNERS = 2
    CREDITORS = 3
    ACCESS_TYPES = [
        (SUPERUSER, 'Суперпользователь'),
        (PARTNERS, 'Партнер'),
        (CREDITORS, 'Кредитная организация'),
    ]
    access_type = models.IntegerField(choices=ACCESS_TYPES, null=True, blank=True)


class CreationInfo(models.Model):
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name='Дата и время создания')

    class Meta:
        abstract = True


class ChangingInfo(CreationInfo):
    changed_at = models.DateTimeField(
        default=timezone.now,
        verbose_name='Дата и время изменения')

    class Meta:
        abstract = True


class Organization(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'


class Offer(ChangingInfo):
    CATEGORIES = (
        ('C', 'потребительский'),  # consumer credit
        ('M', 'ипотека'),          # mortgage
        ('A', 'автокредит'),       # auto loan
        ('S', 'КМСБ'),             # SME finance
    )

    started_rotating_at = models.DateTimeField(
        verbose_name='Дата и время начала ротации')
    ended_rotating_at = models.DateTimeField(
        verbose_name='Дата и время окончания ротации')
    name = models.CharField(max_length=100,
                            verbose_name='Название')
    category = models.CharField(max_length=1, choices=CATEGORIES,
                                verbose_name='Тип')
    min_score = models.IntegerField(
        validators=CREDIT_SCORE_VALIDATORS,
        verbose_name='Минимальны скоринговый балл',
    )
    max_score = models.IntegerField(
        validators=CREDIT_SCORE_VALIDATORS,
        verbose_name='Максимальный скоринговый балл',
    )
    organization = models.ForeignKey(Organization)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Предложение'
        verbose_name_plural = 'Предложения'


class CustomerProfile(ChangingInfo):

    first_name = models.CharField(max_length=100, verbose_name='Имя')
    patronymic = models.CharField(max_length=100, verbose_name='Отчество')
    surname = models.CharField(max_length=100, verbose_name='Фамилия')
    birth_day = models.DateField(verbose_name='День рождения')
    phone = PhoneNumberField(verbose_name='Телефон')
    passport_number = models.CharField(max_length=10, verbose_name='Номер паспорта')
    score = models.IntegerField(
        validators=CREDIT_SCORE_VALIDATORS,
        null=True,
        blank=True,
        default=0,
        verbose_name='Скоринговый балл',
    )

    @property
    def fio(self):
        return ' '.join([self.surname, self.first_name, self.patronymic])

    def __str__(self):
        return self.fio

    class Meta:
        verbose_name = 'Анкета клиента'
        verbose_name_plural = 'Анкеты клиентов'


class Application(CreationInfo):
    STATUS_NEW = 'NEW'
    STATUS_SENT = 'SENT'
    STATUS_RECEIVED = 'RECEIVED'

    STATUSES = (
        (STATUS_NEW, 'новая'),
        (STATUS_SENT, 'отправленная'),
        (STATUS_RECEIVED, 'принятая'),
    )

    sent_at = models.DateTimeField(default=timezone.now,
                                   verbose_name='Дата и время отправки')
    customer_profile = models.ForeignKey(CustomerProfile,
                                         verbose_name='Анкета клиента',
                                         on_delete=models.CASCADE)
    offer = models.ForeignKey(Offer, verbose_name='Кредитное предложение')
    status = models.CharField(max_length=10, choices=STATUSES, default=STATUS_NEW,
                              verbose_name='Статус')

    def __str__(self):
        return '{} - {}'.format(self.customer_profile.fio, self.offer)

    class Meta:
        verbose_name = 'Заявка в кредитную организацию'
        verbose_name_plural = 'Заявки в кредитные организации'
        unique_together = ('customer_profile', 'offer')
