import os
import requests
import json
from datetime import datetime
from calendar import monthrange
import telebot

year = 2023
token = os.getenv('TOKEN')

bot = telebot.TeleBot(token)

#получение праздничных и выходных дней
def __calendar(month):
    #Получить список дат
    req = requests.get(f'http://xmlcalendar.ru/data/ru/{year}/calendar.json')
    json_req = json.loads(req.text)
    list_date = json_req['months']
    #print(list_date)
    #парсинг
    #Выбрать месяц
    #Добавить к month - 1
    month_add = month - 1
    #Добавление days для отображения дат
    month_result = list_date[month_add]['days']
    #print(month_result)
    #обернуть month_result в лист
    month_result_list = month_result.split(",")
    list(month_result_list)
    #print(month_result_list)
    #исключить из массива даты со спец знаком.
    #Добавляем новый массив
    month_result_update = []
    #делаем поиск предпразничных и праздничных дней
    for i in month_result_list:
        if  i.find('+') == 2:
            #если находи цифру с +, тогда добавляем в массив
            month_result_update.append(int(i.replace("+", "")))
        elif i.find('*') == 2:
            # если находи цифру с *, тогда добавляем в массив
            month_result_update.append(int(i.replace("*", "")))
        else:
            month_result_update.append(int(i))
    print(month_result_update)
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
    print("func_date")
    # print(month)
    # print(month_days)

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

    # print(mass_1)

    # вторая половина месяца
    num = 16
    for i in range(day_2):
        mass_2.append(num)
        num += 1

    print(mass_2)

    # убрать выходные
    print('выхи')
    # за первую половину 15 дней
    result_day_1 = list(set(mass_1) - set(month_days))

    print(mass_1)
    print(month_days)
    print(result_day_1)

    # за вторую половину

    result_day_2 = list(set(mass_2) - set(month_days))
    print(mass_2)
    print(result_day_2)
    return result_day_1, result_day_2



res = __calendar(2)

print(res[1])


res_ = number_month(2)
print(res_)

#print(res_ - res)

def extract_arg(arg):
    return arg.split()[1:]

mass_messsage = []
month_list = ['январь', 'май', 'март', 'апрель', 'май', 'июнь',
           'июль', 'август', 'сентябрь', 'октябрь', 'ноябрь', 'декабрь']

@bot.message_handler(commands=["start"])
def start(mesage):
    bot.send_message(mesage.chat.id,"Привет ✌ \n Введите команду /calculate \n и передайте два параметра\n Пример: /calculate Май 100")

@bot.message_handler(commands=["calculate"])
def start(message):
    status = extract_arg(message.text)
    print(status)
    #if is_int(status[0]) ==
    if len(status) != 0:

        if month_list.count(status[0]) > 0:
            if len(status) == 2:
                if is_int(status[1]) == True:
                    #количество праздничных дней
                    int_num = month_list.index(status[0]) + 1
                    #resutl_days_job = __calendar(int_num)

                    # количество дней в месяце
                    res_days_month = number_month(int_num)

                    #количество выходных дней
                    res_days_calendar = __calendar(int_num)

                    # получить количество рабочих дней
                    res_job_days = func_date(res_days_month, res_days_calendar)
                    res_job_days_sum = len(res_job_days[1]) + len(res_job_days[0])

                    # количество рабочих дней за весь месяц
                    # за первую половину месяца
                    res_job_month_15_1 = len(res_job_days[0])
                    # за вторую половину месяца
                    res_job_month_15_2 = len(res_job_days[1])

                    res_job_month_sum = res_job_month_15_1 + res_job_month_15_2

                    #считаем зарплату - 13%
                    res_okld = int(status[1]) / 100 * 13
                    res__okld_proc = int(status[1]) - res_okld

                    # считаем оплату за день
                    result_days_oklad_days = int(res__okld_proc / res_job_month_sum)

                    # Оплата за первую и вторую половину месяца
                    result_month_zp_1 = result_days_oklad_days * res_job_month_15_1
                    result_month_zp_2 = result_days_oklad_days * res_job_month_15_2

                    #resutl_days = res_ - resutl_days_job[0]
                    #res_okld = int(status[1]) / 100 * 13
                    #res__okld_proc = int(status[1]) - res_okld

                    #result_days_oklad_days = int(res__okld_proc / resutl_days)

                    #print(resutl_days_job[0])
                    #print(int_num)

                    #получить количество рабочих дней

                    #оплата за первую половину месяца


                    #оплата за вторую половину месяца

                    bot.send_message(message.chat.id, f"Количество дней в месяце {str(res_days_month)}\nКоличество праздничных и выходных дней: {len(res_days_calendar)}\nКоличество рабочих дней: {res_job_days_sum}\nКоличество рабочих дней за первую половину: {res_job_month_15_1}\nКоличество рабочих дней за вторую половину: {res_job_month_15_2}\nОплата за первую половину месяца: {result_month_zp_1}\nОлпата за вторую половину месяца: {result_month_zp_2}\nОклад (-13%): {str(res__okld_proc)}\nОплата в день: {str(result_days_oklad_days)}\n" )
                else:
                    bot.send_message(message.chat.id, "Неккоретный параметр оклад")
        elif len(status) == 1:
            bot.send_message(message.chat.id, "Неккоретный параметр оклад")
        else:
            bot.send_message(message.chat.id, "Неккоретный параметр месяц")




@bot.message_handler(content_types=["text"])
def echo_all(message):
    bot.send_message(message.chat.id,"Я не понял")



bot.polling()