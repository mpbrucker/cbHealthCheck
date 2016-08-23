#!/usr/bin/python

from cbapi.response.models import Sensor
from cbapi.response.rest_api import CbEnterpriseResponseAPI
from datetime import date
import operator
import smtplib
from email.mime.text import MIMEText
import email.utils
import datetime
import consts

import logging

logging.basicConfig(level=logging.DEBUG)
c = CbEnterpriseResponseAPI()

sender = consts.SENDER
receivers = consts.RECEIVERS
smtp_serv = consts.SMTP


def main():
    health_dict = {}
    obj = c.select(Sensor)
    print date.today()
    for sens in obj:
        last_up = sens.last_update.split(' ')[0]
        diff = diff_days(str(date.today()), last_up)
        if diff < 8:
            split_str = sens.computer_name.split('.')[0]
            health_dict[split_str] = sens.sensor_health_status
    new_dict = sorted(health_dict.items(), key=operator.itemgetter(1))

    most_sick = []
    for y in range(0, 5):
        most_sick.append(new_dict[y])

    sick_list = ['Top 5 sickest machines: ']
    for x in most_sick:
        list_join = ['Sensor name:', x[0], 'Health score:', repr(x[1])]
        sick_str = ' '.join(list_join)
        sick_list.append(sick_str)

    new_str = '\n'.join(sick_list)
    msg = MIMEText(new_str)

    msg['To'] = email.utils.formataddr(('Security', receivers[0]))
    msg['From'] = email.utils.formataddr(('Carbon Black Alerts', sender))
    msg['Subject'] = 'Carbon Black Sensor Health Check ' + str(datetime.date.today())

    smtp_obj = smtplib.SMTP(smtp_serv, 25)
    smtp_obj.sendmail(sender, receivers, msg.as_string())
    smtp_obj.quit()


def diff_days(date1, date2):
    day1_split = date1.split('-')
    day2_split = date2.split('-')
    day1_val = int(day1_split[0])*365 + int(day1_split[1])*30.5 + int(day1_split[2])
    day2_val = int(day2_split[0])*365 + int(day2_split[1])*30.5 + int(day2_split[2])
    return int(abs(day2_val-day1_val))


main()
