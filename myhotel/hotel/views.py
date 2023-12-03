import datetime
from operator import itemgetter

from django.urls import reverse
from django.shortcuts import render, redirect
from django.db import connection
from . import views
from .forms import UploadFileForm, AddPostForm
from .models import Client, Employees
from django.template.loader import render_to_string
import collections
menu = [

    {'title': "Регистрация клиента", 'url_name': 'add_client'},
    {'title': "График дежурства", 'url_name': 'duty_schedule'},
    {'title': "Обслуживающий персонал", 'url_name': 'service_room'},
    {'title': "Распределение номеров", 'url_name': 'number_distribution'},
    {'title': "Редактор номеров", 'url_name': 'redactor_number'},
    {'title': "Редактор категорий", 'url_name': 'redactor_category'},
]


def index(request):
    data = {
        'title': 'Приложение для администратора гостиницы',
        'menu': menu,
    }
    return render(request, 'hotel/index.html', data)


def client_post(request):
    if 'save' in request.POST:
        famille = str(request.POST['famille'])
        firstName = str(request.POST.get('firstName'))
        lastName = request.POST.get('lastName')
        birthday = request.POST.get('birthday')
        passport = request.POST.get('passport')
        city = request.POST.get('city')
        street = request.POST.get('street')
        home = request.POST.get('home')
        apartment = request.POST.get('apartment')
        number_hotel = request.POST.get('number_hotel')
        date_arrival = request.POST.get('date_arrival')
        date_departure = request.POST.get('date_departure')

        with connection.cursor() as cursor:
            cursor.execute(
                f'SELECT * from hotel_client where passport = "{passport}"')
            row = cursor.fetchall()
            global pas  # без этого костыля не работает
            pas = 'Нечто'
            for v in row:
                pas = v[6]
            if str(pas) != str(passport):
                cursor.execute(
                    'INSERT INTO hotel_client (famille, firstName, lastName, birthday, passport, city, street, home, '
                    'apartment)'
                    f'VALUES ("{famille}","{firstName}","{lastName}","{birthday}","{passport}","{city}","{street}","{home}","{apartment}")')

                cursor.execute(f'SELECT client_id from hotel_client where passport = "{passport}"')
                row = cursor.fetchone()
                client_id = row[0]
                cursor.execute(f'SELECT number_id from hotel_number where number = "{number_hotel}"')
                row = cursor.fetchone()
                number_id = row[0]
                cursor.execute(
                    'INSERT INTO hotel_numberdistribution (number_id, client_id, time_arrival, time_departure)'
                    f'VALUES ("{number_id}", "{client_id}", "{date_arrival}", "{date_departure}")'
                )


def add_client(request):
    data = {
        'title': 'Регистрация клиента',
        'menu': menu,
    }
    client_post(request)
    return render(request, 'hotel/add_client.html', data)


def create_duty_schedule(request):
    if 'save' in request.POST:
        work_day = request.POST.get('work_day')
        number_hotel = request.POST.get('number_hotel')
        famille = request.POST.get('famille')
        if work_day != "" and number_hotel != "" and famille != "":
            with connection.cursor() as cursor:
                cursor.execute(
                    f'SELECT * from hotel_employees where familleEmp = "{famille}"'
                )
                row = cursor.fetchone()
                v = row[0]
                cursor.execute(
                    f'SELECT * from hotel_number where number = "{number_hotel}"'
                )
                row = cursor.fetchone()
                n = row[0]
                cursor.execute(
                    'INSERT INTO hotel_roomservice (employees_id, number_id, work_day)'
                    f'VALUES ("{v}", "{n}", "{work_day}")'
                )

    if 'delete' in request.POST:
        room_id = request.POST.get('room_id')
        print(room_id)
        with connection.cursor() as cursor:
            cursor.execute(
                f'DELETE FROM hotel_roomservice WHERE room_id = "{room_id}"'
            )

    if 'update' in request.POST:
        work_day = request.POST.get('work_day')
        number_hotel = request.POST.get('number_hotel')
        famille = request.POST.get('famille')
        room_id = request.POST.get('room_id')
        if work_day != "" and number_hotel != "" and famille != "" and room_id != "":
            with connection.cursor() as cursor:
                cursor.execute(
                    f'SELECT * from hotel_employees where familleEmp = "{famille}"'
                )
                row = cursor.fetchone()
                v = row[0]
                cursor.execute(
                    f'SELECT * from hotel_number where number = "{number_hotel}"'
                )
                row = cursor.fetchone()
                n = row[0]

                cursor.execute(
                    f'SELECT * from hotel_roomservice WHERE room_id = "{room_id}"'
                )
                row = cursor.fetchone()
                k = row[0]
                cursor.execute(
                    f'UPDATE hotel_roomservice SET employees_id="{v}", number_id="{n}", work_day="{work_day}" WHERE '
                    f'room_id="{k}"'
                )


def duty_schedule(request):
    create_duty_schedule(request)
    with connection.cursor() as cursor:
        cursor.execute(
            f'SELECT room_id, familleEmp, photo, number_id, work_day FROM hotel_employees, hotel_roomservice   WHERE '
            f'hotel_employees.id = hotel_roomservice.employees_id ORDER BY work_day'
        )
        rows = []
        for row in cursor.fetchall():
            rows.append({
                'room_id': str(row[0]),
                'familleEmp': str(row[1]),
                'photo': str(row[2]),
                'number_id': str(row[3]),
                'work_day': str(row[4])
            })
    return render(request, 'hotel/duty_schedule.html',
                  {'title': 'График дежурства сотрудников', 'menu': menu, 'rows': rows})


def room(request):
    if 'saveEmp' in request.POST:
        with connection.cursor() as cursor:
            cursor.execute(
                f'SELECT id FROM hotel_employees ORDER BY Id DESC LIMIT 1')
            row = cursor.fetchone()

            v = row[0]
            print(v)
            familleEmp = request.POST.get('familleEmp')
            firstNameEmp = request.POST.get('firstNameEmp')
            lastNameEmp = request.POST.get('lastNameEmp')
            cityEmp = request.POST.get('cityEmp')
            streetEmp = request.POST.get('streetEmp')
            homeEmp = request.POST.get('homeEmp')
            apartmentEmp = request.POST.get('apartmentEmp')
            phone = request.POST.get('phone')
            print(familleEmp)
            with connection.cursor() as cursor:
                cursor.execute(
                    f'UPDATE hotel_employees SET familleEmp="{familleEmp}", firstNameEmp="{firstNameEmp}", '
                    f'lastNameEmp="{lastNameEmp}", cityEmp="{cityEmp}", streetEmp="{streetEmp}", '
                    f'homeEmp="{homeEmp}", apartmentEmp="{apartmentEmp}", phone="{phone}" WHERE id="{v}"'
                )


def service_room(request):  # обслуживающий персонал добавление
    if request.method == 'POST':
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    else:
        form = AddPostForm()
    room(request)
    return render(request, 'hotel/service_room.html', {'title': 'Обслуживающий персонал', 'menu': menu, 'form': form})


def create_number(request):
    if 'save_number' in request.POST:
        number = request.POST.get('number')
        count_place = request.POST.get('count_place')
        descript = request.POST.get('descript')
        price = request.POST.get('price')
        category = request.POST.get('category')
        with connection.cursor() as cursor:
            cursor.execute(
                'INSERT INTO hotel_number (number, numberOfPlaces,description,pricePerDay,category_id)'
                f'VALUES ("{number}", "{count_place}", "{descript}", "{price}", "{category}")'
            )


def redactor_number(request):
    create_number(request)
    return render(request, 'hotel/redactor_number.html', {'title': 'Редактор номеров', 'menu': menu})


def create_category(request):
    if 'save_category' in request.POST:
        category = request.POST.get('category')
        with connection.cursor() as cursor:
            cursor.execute(
                'INSERT INTO hotel_category (name)'
                f'VALUES ("{category}")'
            )


def redactor_category(request):
    create_category(request)
    return render(request, 'hotel/redactor_category.html', {'title': 'Редактор категорий', 'menu': menu})


def number_distribution(request):
    if 'show' in request.POST:
        time_arrival = request.POST.get('time_arrival')
        date_arrival = datetime.datetime.strptime(time_arrival, '%Y-%m-%d')
        time_departure = request.POST.get('time_departure')
        date_departure = datetime.datetime.strptime(time_departure, '%Y-%m-%d')
        with connection.cursor() as cursor:
            cursor.execute(
                f'SELECT number_id FROM hotel_numberdistribution WHERE NOT'
                f'(time_arrival BETWEEN "{date_arrival}" AND "{date_departure}"'
                f'OR time_departure BETWEEN "{date_arrival}" AND "{date_departure}")'
            )
            rows = []
            for row in cursor.fetchall():
                rows.append({'number_id': str(row[0])})
            # print(rows)

            cursor.execute(
                f'SELECT hotel_number.number_id FROM hotel_number LEFT JOIN hotel_numberdistribution ON '
                f'hotel_number.number_id = hotel_numberdistribution.number_id WHERE '
                f'hotel_numberdistribution.number_id IS NULL'
            )
            numbers = cursor.fetchall()
            numbers = ([t for t in (set(int(i[0]) for i in numbers))])
            row = []

            for i in numbers:
                row.append({'number_id': str(i)})
            # print(row)
            rows = rows + row
            cursor.execute(
                f'SELECT number_id, name FROM hotel_number, hotel_category WHERE '
                f'hotel_number.category_id = hotel_category.id'
            )
            rows_category = []
            for row in cursor.fetchall():
                rows_category.append({
                    'number_id': str(row[0]),
                    'category': str(row[1])
                })
            for row in rows:
                for row_category in rows_category:
                    if row['number_id'] == row_category['number_id']:
                        cat = row_category['category']
                        row['category'] = cat
            rows = sorted(rows, key=itemgetter('number_id'))
            print(rows)

    else:
        with connection.cursor() as cursor:
            cursor.execute(
                f'SELECT famille, number_id, current_date FROM hotel_client, hotel_numberdistribution WHERE '
                f'hotel_client.client_id = hotel_numberdistribution.client_id'
            )
            rows = []
            for row in cursor.fetchall():
                rows.append({
                    'famille': str(row[0]),
                    'number_id': str(row[1]),
                    'current_date': str(row[2])
                })
            cursor.execute(
                f'SELECT number_id, name FROM hotel_number, hotel_category WHERE '
                f'hotel_number.category_id = hotel_category.id'
            )
            rows_category = []
            for row in cursor.fetchall():
                rows_category.append({
                    'number_id': str(row[0]),
                    'category': str(row[1])
                })
            current_date = str(datetime.date.today().isoformat())
            rows_emp = []
            cursor.execute(
                f'SELECT familleEmp, photo, number_id FROM hotel_employees, hotel_roomservice   WHERE '
                f'hotel_employees.id = hotel_roomservice.employees_id AND work_day = "{current_date}"'
            )
            for row in cursor.fetchall():
                rows_emp.append({
                    'familleEmp': str(row[0]),
                    'photo': str(row[1]),
                    'number_id': str(row[2])
                })
            # print(rows_emp)
            for row in rows:
                for row_emp in rows_emp:
                    if row['number_id'] == row_emp['number_id']:
                        familleEmp = row_emp['familleEmp']
                        photo = row_emp['photo']
                        row['familleEmp'] = familleEmp
                        row['photo'] = photo

            for row in rows:
                for row_category in rows_category:
                    if row['number_id'] == row_category['number_id']:
                        cat = row_category['category']
                        row['category'] = cat
    print(rows)
    return render(request, 'hotel/number_distribution.html', {'title': 'Распределение номеров', 'menu': menu, 'rows': rows})
