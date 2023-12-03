from django.db import models
from django.db.models.functions import datetime
from django.utils import timezone


class Client(models.Model): # модель описывающая клиента гостиницы
    title = models.CharField(max_length=250, null=True, verbose_name='Клиенты') # заголовок
    famille = models.CharField(max_length=20, db_index=True, null=True, verbose_name="Фамилия") # фамилия
    firstName = models.CharField(max_length=20, null=True, verbose_name="Имя") # имя
    lastName = models.CharField(max_length=20, null=True, verbose_name="Отчество") # отчество
    birthday = models.DateField(auto_now=False, auto_now_add=False, null=True, verbose_name="Дата рождения") # день рождения
    passport = models.IntegerField(default=0, verbose_name="Серия и номер паспорта") # серия номер паспорта одним числом 10 знаков
    city = models.CharField(max_length=20, null=True, verbose_name="Город проживания") # город
    street = models.CharField(max_length=20, null=True, verbose_name="Улица") # улица
    home = models.IntegerField(default=0,verbose_name="номер дома")
    apartment = models.IntegerField(default=0, verbose_name="Номер квартиры") # номер квартиры
    current_date = models.DateTimeField(timezone.now, null=True)

    def __str__(self):
        return self.title


class Number(models.Model):# модель описывающая номер в гостинице
    number = models.IntegerField(default=0, db_index=True, unique=True, verbose_name='Номер')
    numberOfPlaces = models.IntegerField(default=0,verbose_name="Количество мест в номере")
    description = models.TextField(blank=True, verbose_name="Описание номера")
    pricePerDay = models.IntegerField(default=0, verbose_name="Стоимость номера в сутки")
    category = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name="Категории") # связь с таблицей Категория одна категория - номеров много связь many to one


    def __str__(self):
        return self.number


class NumberDistribution(models.Model): # модель описывающая распределение номеров
    client = models.ForeignKey('Client', on_delete=models.SET_NULL, null=True, verbose_name="Клиент")
    number = models.ForeignKey('Number', on_delete=models.SET_NULL,  null=True, verbose_name="Номер гостиницы")
    time_arrival = models.DateField(null=True, verbose_name="Дата заезда") # дата прибытия
    time_departure = models.DateField(null=True, verbose_name="Дата выезда") # дата убытия


class Category(models.Model):
    name = models.CharField(max_length=20, db_index=True, verbose_name="Категория")

    def __str__(self):
        return self.name


class Employees(models.Model): # класс описывающий сотрудников
    familleEmp = models.CharField(max_length=20, db_index=True, null=True, verbose_name="Фамилия")  # фамилия
    firstNameEmp = models.CharField(max_length=20, null=True, verbose_name="Имя")  # имя
    lastNameEmp = models.CharField(max_length=20, null=True, verbose_name="Отчество")  # отчество
    cityEmp = models.CharField(max_length=20, null=True, verbose_name="Город проживания")  # город
    streetEmp = models.CharField(max_length=20, null=True, verbose_name="Улица")  # улица
    homeEmp = models.IntegerField(default=0, verbose_name="номер дома")
    apartmentEmp = models.IntegerField(default=0, verbose_name="Номер квартиры")  # номер квартиры
    phone = models.CharField(max_length=11, default=0, verbose_name="Номер телефона")
    photo = models.ImageField(upload_to="photos", default=None,
                              blank=True,null=True,verbose_name='Фото')


class RoomService(models.Model): # Модель описывающая обслуживание номеров
    number = models.ForeignKey('Number', on_delete=models.SET_NULL, null=True, verbose_name="Номер гостиницы") # связь с таблицей Номер
    employees = models.ForeignKey('Employees', on_delete=models.SET_NULL, null=True, verbose_name="Код сотрудника") # связь с таблицей Сотрудники
    work_day = models.DateField(auto_now=False, auto_now_add=False, null=True, verbose_name="День рабочей смены")

