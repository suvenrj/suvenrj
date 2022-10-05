import xlwings as xw
import time
from datetime import datetime
from alright import WhatsApp
import json

clinic_details = open('clinic_detail.txt',  'r')
clinic_details_list = clinic_details.readlines()
clinic_name = clinic_details_list[0]
clinic_review_link = clinic_details_list[1]
clinic_map_link=clinic_details_list[2]
clinic_excel_sheet=clinic_details_list[3]

try:
    json_file=open("common_dict.json", "r+")
    dict_data=json.load(json_file)
    has_person_been_texted_3=dict_data["worksheet.xlsx"]["has_person_been_texted_3"]
    has_person_been_texted_5=dict_data["worksheet.xlsx"]["has_person_been_texted_5"]
    has_person_been_sent_welcome=dict_data["worksheet.xlsx"]["has_person_been_sent_welcome"]
    has_person_been_sent_review_link=dict_data["worksheet.xlsx"]["has_person_been_sent_review_link"]
    json_file.close()
except:
    json_file=open("common_dict.json", "r+")
    dict_data=json.load(json_file)
    excel_file_dict={"has_person_been_sent_review_link": {}, "has_person_been_sent_welcome": {}, "has_person_been_texted_3": {}, "has_person_been_texted_5": {}}
    dict_to_be_added={"worksheet.xlsx": excel_file_dict}
    dict_data.update(dict_to_be_added)
    json_file.seek(0)
    json.dump(dict_data, json_file)
    json_file.close()
    has_person_been_texted_3 = {}
    has_person_been_texted_5 = {}
    has_person_been_sent_welcome = {}
    has_person_been_sent_review_link = {}

#has_person_been_texted_3 = {}
#has_person_been_texted_5 = {}
#has_person_been_sent_welcome = {}
#has_person_been_sent_review_link = {}

# B- patient name, C- mobile number, D- status, E-time

messenger = WhatsApp()


def position_of_waiting_patient(ws, n, position_to_be_found):
    count = 0
    for j in range(2, n+1):
        index_of_done = 'D'+str(j)
        if ws.range(index_of_done).value == None:
            count += 1
        if count == position_to_be_found:
            return j
    return -1


def number_of_patients(ws):
    number = 0
    for i in range(1, 1000):
        temp_index = 'C'+str(i)
        if ws.range(temp_index).value == None:
            return number
        else:
            number += 1
    return 0

def str_to_time(ws, j):
    index='E'+str(j)
    time = ws.range(index).value
    hours= str(int((time*24)//1))
    minutes= str(int((((time*24) % 1)*60)//1))
    return int(hours) , int(minutes)
def appointment_duration(ws, j):
    initial_hours, initial_minutes = str_to_time(ws, j)
    final_hours, final_minutes= str_to_time(ws, j+1)
    duration_hours= final_hours-initial_hours
    duration_minutes = final_minutes-initial_minutes
    if (duration_minutes<0):
        duration_minutes+=60
        duration_hours-=1
    return duration_hours, duration_minutes
def update():
    wb = xw.Book("worksheet.xlsx")
    ws = wb.sheets[0]
    messages_arr = []
    phone_number_arr = []
    from datetime import datetime

    now = datetime.now()
    current_time = now.strftime("%H:%M")

    # In the first loop, we use j for phone number which is bad for consistency and readability
    n = number_of_patients(ws)
    for theta in range(2, n+1):
        phone_number_index = 'C'+str(theta)
        time_index = 'E'+str(theta)
        temp_time = (ws.range(time_index).value)
        temp_hours = str(int((temp_time*24)//1))
        temp_minutes = str(int((((temp_time*24) % 1)*60)//1))
        if len(temp_hours) == 1:
            temp_hours = '0'+temp_hours
        if len(temp_minutes) == 1:
            temp_minutes = '0'+temp_minutes
        final_time = str(temp_hours)+":"+str(temp_minutes)
        j = str(int(ws.range(phone_number_index).value))
        if j not in has_person_been_texted_3:
            has_person_been_texted_3[j] = False  # j is our phnone number
            has_person_been_sent_review_link[j] = False
            has_person_been_texted_5[j] = False
        if j not in has_person_been_sent_welcome:
            has_person_been_sent_welcome[j] = True
            phone_number_arr.append(str(j))

            messages_arr.append("Hello, your appointment at " + str(clinic_name) + " is scheduled at "+str(final_time))
    count = 0
    for j in range(2, n+1):
        index_of_done = 'D'+str(j)
        if ws.range(index_of_done).value == None:
            count += 1
            if count == 3:
                phone_number_index = 'C'+str(j)
                temp_phone_number = str(int(ws.range(phone_number_index).value))
                #time_index = 'E'+str(j)
                #temp_time = (ws.range(time_index).value)
                #temp_time_prev = (ws.range(time_index_prev).value)
                # temp_hours = (temp_time*24)//1
                # temp_minutes = (((temp_time*24) % 1)*60)//1
                if has_person_been_texted_3[temp_phone_number] == False:
                    has_person_been_texted_3[temp_phone_number] = True
                    phone_number_arr.append(temp_phone_number)
                    # now = datetime.now()
                    current_time_hour = int(now.strftime("%H"))
                    current_time_minutes = int(now.strftime("%M"))
                    # current_time_float = current_time_hour / (24)
                    # current_time_float += (current_time_minutes/(60*24))
                    # best_float = max(current_time_float+1/48, temp_time)
                    start_time_hour, start_time_minute = str_to_time(ws, j)
                    duration_hour_1, duration_minute_1 = appointment_duration(ws,position_of_waiting_patient(ws, n, 1))
                    duration_hour_2, duration_minute_2 = appointment_duration(ws,position_of_waiting_patient(ws, n, 2))
                    final_hours=start_time_hour+duration_hour_1+duration_hour_2
                    final_minutes=start_time_minute+duration_minute_1+duration_minute_2
                    if (final_minutes>59):
                        final_minutes-=60
                        final_hours+=1
                    final_hours = str(final_hours)
                    final_minutes = str(final_minutes)
                    if len(final_hours) == 1:
                        final_hours = '0'+final_time_hours
                    if len(final_time_minutes) == 1:
                        final_minutes = '0'+final_minutes
                    final_time = str(final_hours)+":" + str(final_minutes)
                    message_to_be_sent = "Hello, there are 2 people ahead of you. Please come at "
                    message_to_be_sent += str(final_time)
                    messages_arr.append(message_to_be_sent)
            if count == 5:
                phone_number_index = 'C'+str(j)
                temp_phone_number = str(int(ws.range(phone_number_index).value))
                # temp_hours = (temp_time*24)//1
                # temp_minutes = (((temp_time*24) % 1)*60)//1
                if has_person_been_texted_5[temp_phone_number] == False:
                    has_person_been_texted_5[temp_phone_number] = True
                    phone_number_arr.append(temp_phone_number)
                    # now = datetime.now()
                    current_time_hour = int(now.strftime("%H"))
                    current_time_minutes = int(now.strftime("%M"))
                    # current_time_float = current_time_hour / (24)
                    # current_time_float += (current_time_minutes/(60*24))
                    # best_float = max(current_time_float+1/48, temp_time)
                    start_time_hour, start_time_minute = str_to_time(ws, j)
                    duration_hour_1, duration_minute_1 = appointment_duration(ws,position_of_waiting_patient(ws, n, 3))
                    duration_hour_2, duration_minute_2 = appointment_duration(ws,position_of_waiting_patient(ws, n, 4))
                    final_hours=start_time_hour+duration_hour_1+duration_hour_2
                    final_minutes=start_time_minute+duration_minute_1+duration_minute_2
                    if (final_minutes>59):
                        final_minutes-=60
                        final_hours+=1
                    final_hours = str(final_hours)
                    final_minutes = str(final_minutes)
                    if len(final_hours) == 1:
                        final_hours = '0'+final_hours
                    if len(final_minutes) == 1:
                        final_minutes = '0'+final_minutes
                    final_time = str(final_hours)+":" + str(final_minutes)
                    message_to_be_sent = "Hello, there are 4 people ahead of you. Please come at "
                    message_to_be_sent += str(final_time)
                    messages_arr.append(message_to_be_sent)

    for j in range(2, n+1):
        index_of_done = 'D'+str(j)
        if ws.range(index_of_done).value == "DONE":
            phone_number_index = 'C'+str(j)
            temp_phone_number = str(int(ws.range(phone_number_index).value))
            if has_person_been_sent_review_link[temp_phone_number] == False:
                has_person_been_sent_review_link[temp_phone_number] = True
                phone_number_arr.append(temp_phone_number)
                messages_arr.append(str(clinic_review_link))

    return phone_number_arr, messages_arr


while (True):
    time.sleep(10)
    phone_number_arr, messages_arr = update()
    l = len(phone_number_arr)
    for i in range(l):
        messenger.find_by_username(phone_number_arr[i])
        messenger.send_message(messages_arr[i])
    json_file=open("common_dict.json", "r+")
    dict_data=json.load(json_file)
    excel_file_dict={"has_person_been_sent_review_link": has_person_been_sent_review_link}
    excel_file_dict["has_person_been_sent_welcome"]=has_person_been_sent_welcome
    excel_file_dict["has_person_been_texted_3"]=has_person_been_texted_3
    excel_file_dict["has_person_been_texted_5"]=has_person_been_texted_5
    dict_to_be_added={"worksheet.xlsx": excel_file_dict}
    dict_data.update(dict_to_be_added)
    json_file.seek(0)
    json.dump(dict_data, json_file)
    json_file.close()