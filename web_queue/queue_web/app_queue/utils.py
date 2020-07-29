import time
from app_queue import models
from django.db.models import Min, Max


def max_order_id(database_model):
    order_id_dict = database_model.objects.aggregate(Max('order_id'))
    return order_id_dict['order_id__max']


def min_order_id(database_model):
    order_id_dict = database_model.objects.aggregate(Min('order_id'))
    return order_id_dict['order_id__min']




def new_order_id(database_model):
    order_id_dict = database_model.objects.aggregate(Max('order_id'))
    order_id = order_id_dict['order_id__max']
    if order_id:
        order_id += 1
    else:
        order_id = 1

    return order_id


def database_add_one(database_model, data_dict):
    user_obj = database_model(**data_dict)
    user_obj.save()


def get_first_mission(database_model):
    obj = database_model.objects.all().order_by("order_id").first()
    return obj


def move_to_running(obj):
    data_dict = obj.get_data_dict()
    data_dict.pop('id')
    data_dict.pop('order_id')
    database_add_one(models.RunningList, data_dict)
    obj.delete()


def take_task(database_model):
    while True:
        first_obj = get_first_mission(database_model)
        if first_obj:
            move_to_running(first_obj)
        else:
            print('empty')

        time.sleep(5)




