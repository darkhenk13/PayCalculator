from app import *

year = 2023

#получение праздничных и выходных дней
def __calendar(month):
    #Получить список дат
    req = requests.get(f'http://xmlcalendar.ru/data/ru/{year}/calendar.json')
    json_req = json.loads(req.text)
    list_date = json_req['months']
    #парсинг
    #Выбрать месяц
    #Добавить к month - 1
    month_add = month - 1
    #Добавление days для отображения дат
    month_result = list_date[month_add]['days']
    #обернуть month_result в лист
    month_result_list = month_result.split(",")
    list(month_result_list)
    #исключить из массива даты со спец знаком.
    #Добавляем новый массив
    month_result_update = []
    #делаем поиск предпразничных и праздничных дней
    for i in month_result_list:
        if i.find('+') == 2:
            #если находи цифру с +, тогда добавляем в массив
            month_result_update.append(int(i.replace("+", "")))
        elif i.find('*') == 2:
            # если находи цифру с *, тогда добавляем в массив
            month_result_update.append(int(i.replace("*", "")))
        else:
            month_result_update.append(int(i))
    return month_result_update


# количество дней в месяце
def number_month(month):
    current_year = datetime.now().year
    days = monthrange(current_year, month)[1]
    return days


def is_int(str):
    try:
        int(str)
        return True
    except ValueError:
        return False


def func_date(month, month_days):
    mass_1 = []  # массив для формирования рабочих дней
    mass_2 = []  # массив для формирования рабочих дней
    mass_month = []  # массив для формирования дней по месяцам
    # сгенерировать массив с датой
    for i in range(month):
        day = i + 1
        mass_month.append(day)
    # print(mass_month)
    # Разделить на первую половину месяца и на вторую
    day_1 = 15
    day_2 = day - day_1
    # print(day_2)
    # первая половина месяца
    for i in range(day_1):
        mass_1.append(i + 1)
    # вторая половина месяца
    num = 16
    for i in range(day_2):
        mass_2.append(num)
        num += 1
    # убрать выходные
    # за первую половину 15 дней
    result_day_1 = list(set(mass_1) - set(month_days))
    # за вторую половину
    result_day_2 = list(set(mass_2) - set(month_days))
    return result_day_1, result_day_2