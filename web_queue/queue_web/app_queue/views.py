from django.shortcuts import render
from app_queue import models
from app_queue import utils
import datetime
from datetime import timezone
import threading


# Create your views here.
def index(request):
    mission = models.WaitList.objects.all()
    print('index:', mission)
    return render(request, 'index.html')


def add_project(request):
    order_id = utils.new_order_id(models.WaitList)
    data_dict = {'order_id': order_id,
                 'account_email': "zonghui.jin@estra-automotive.com",
                 'sender_address': '10.123.30.23',
                 'mission_name': 'test_demo',
                 'mission_data': "{‘project_address’：'/demo/demo_v1'}",
                 }
    utils.database_add_one(models.WaitList, data_dict)

    return render(request, 'add_project.html')


# b = {'id': 1, 'account_email': 'zonghui.jin@estra-automotive.com', 'sender_address': '10.123.30.23',
#      'mission_name': 'test_demo', 'mission_data': "{‘project_address’：'/demo/demo_v1'}",
#      'register_time': datetime.datetime(2020, 7, 29, 5, 12, 12, 356302, tzinfo= < UTC >)}

def view_history(request):
    return render(request, 'view_history.html')


def setting(request):
    pass
    return render(request, 'setting.html')


a = threading.Thread(target=utils.take_task, args=[models.WaitList, ])
# a.start()


