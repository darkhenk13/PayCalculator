from app import *
from app.logicsBot import calendarLogics



token = os.getenv('TOKEN')

bot = telebot.TeleBot(token)



def extract_arg(arg):
    return arg.split()[1:]

mass_messsage = []
month_list = ['январь', 'май', 'март', 'апрель', 'май', 'июнь',
           'июль', 'август', 'сентябрь', 'октябрь', 'ноябрь', 'декабрь']

@bot.message_handler(commands=["start"])
def start(mesage):
    bot.send_message(mesage.chat.id, "Привет ✌\n Введите команду /calculate\n и передайте два параметра\nПример: /calculate Май 100")


@bot.message_handler(commands=["calculate"])
def start(message):
    status = extract_arg(message.text)
    #print(status)
    if len(status) != 0:
        if month_list.count(status[0]) > 0:
            if len(status) == 2:
                if calendarLogics.is_int(status[1]) == True:
                    #количество праздничных дней
                    int_num = month_list.index(status[0]) + 1
                    # количество дней в месяце
                    res_days_month = calendarLogics.number_month(int_num)
                    #количество выходных дней
                    res_days_calendar = calendarLogics.__calendar(int_num)
                    # получить количество рабочих дней
                    res_job_days = calendarLogics.func_date(res_days_month, res_days_calendar)
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

logging.info('Application start polling telegram')
bot.polling()