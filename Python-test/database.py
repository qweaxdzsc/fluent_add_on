import pymysql

user_name = 'root'
pwd = 'Sdaac=12345'

conn = pymysql.connect(host='localhost',
                       user=user_name,
                       password=pwd,
                       db='cfd-result',
                       charset='utf8mb4'
                    )


def create_login_table(conn, user_name, password):                          # create login verification table
    cursor = conn.cursor()
    sql = """
    CREATE TABLE login (
    id INT auto_increment PRIMARY KEY,
    user_name VARCHAR(20) NOT NULL UNIQUE,
    password VARCHAR(20) NOT NULL
    )ENGINE=innodb DEFAULT CHARSET=utf8mb4;
    """
    cursor.execute(sql)
    cursor.close()

    cursor = conn.cursor()
    insert = """
    insert into login(user_name, password) values(%s,%s);
    """
    cursor.execute(insert, [user_name, password])
    conn.commit()
    cursor.close()


# create_login_table(conn, user_name, pwd)
# test if login success
cursor = conn.cursor()
search = 'select * from login where user_name = "%s" and password ="%s"' % (user_name, pwd)

res = cursor.execute(search)
conn.commit()
cursor.close()

if res:
    print("登录 'cfd-result'数据库 成功")
else:
    print("登录 'cfd-result'数据库 失败")


# start to create cfd-result main table
def create_main_table(conn):
    cursor = conn.cursor()
    main = """
    CREATE TABLE CFD_project (
    ID INT auto_increment PRIMARY KEY,
    Project VARCHAR(45) NOT NULL,
    Version VARCHAR(45) NOT NULL,
    File_address VARCHAR(120) NOT NULL,
    Producer VARCHAR(45) NOT NULL,
    Date DATE NOT NULL,
    RPM SMALLINT NOT NULL,
    Torque float NOT NULL,
    Fan_efficiency float NOT NULL,  
    Total_volume float NOT NULL,
    Total_pressure_loss float NOT NULL       
    )ENGINE=innodb DEFAULT CHARSET=utf8mb4;
    """
    cursor.execute(main)
    cursor.close()


# create volume table
def create_volume_table(conn):
    cursor = conn.cursor()
    volume = """
    CREATE TABLE CFD_volume(
    ID INT auto_increment PRIMARY KEY,
    Project_id INT NOT NULL, 
    constraint fk_volume foreign key(project_id) references CFD_project(id),
    Face_name VARCHAR(45) NOT NULL,
    `Volume(L/S)` float NOT NULL,
    Percentage float NOT NULL
    )ENGINE=innodb DEFAULT CHARSET=utf8mb4;              
    """
    cursor.execute(volume)
    cursor.close()


# create static pressure table
def create_sp_table(conn):
    cursor = conn.cursor()
    sp = """
    CREATE TABLE CFD_sp(
    ID INT auto_increment PRIMARY KEY,
    Project_id INT NOT NULL,
    constraint fk_sp foreign key(project_id) references CFD_project(id),
    Face_name VARCHAR(45) NOT NULL,
    Static_pressure float NOT NULL
    )ENGINE=innodb DEFAULT CHARSET=utf8mb4;              
    """

    cursor.execute(sp)
    cursor.close()


# create total pressure table
def create_tp_table(conn):
    cursor = conn.cursor()
    tp = """
    CREATE TABLE CFD_tp(
    ID INT auto_increment PRIMARY KEY,
    Project_id INT NOT NULL,
    constraint fk_tp foreign key(project_id) references CFD_project(id),
    Face_name VARCHAR(45) NOT NULL,
    Total_pressure float NOT NULL
    )ENGINE=innodb DEFAULT CHARSET=utf8mb4;              
    """

    cursor.execute(tp)
    cursor.close()


# create uniformity
def create_uni_table(conn):
    cursor = conn.cursor()
    uni = """
    CREATE TABLE CFD_uni(
    ID INT auto_increment PRIMARY KEY,
    Project_id INT NOT NULL,
    constraint fk_uni foreign key(project_id) references CFD_project(id),
    Face_name VARCHAR(45) NOT NULL,
    Uniformity float NOT NULL
    )ENGINE=innodb DEFAULT CHARSET=utf8mb4;              
    """

    cursor.execute(uni)
    cursor.close()

# create tables
# create_main_table(conn)
# create_volume_table(conn)
# create_sp_table(conn)
# create_tp_table(conn)
# create_uni_table(conn)

import numpy as np
from txt_to_python import process_data
from fan_efficiency import fan
import time

# decode result data
path = r'G:\GE2_REAR\GE2-rear-round2\GE2-rear-V9-FC\result_GE2-rear2_V9-FC'
new_path = path.replace('\\', '\\\\')
txt_name = path + '\\' + 'GE2-rear2.txt'
print(path)

data_matrix = process_data(txt_name, path)
project_name = 'GE2-rear2'
version = 'V9-FC'
producer = 'zonghui'

rpm = 2850

print(data_matrix)


# insert data into table
def insert_data(conn, data_matrix, project_name, version, file_path, producer, rpm):
    # preprocess data
    c_fan = fan(path, rpm)
    whole_dp = c_fan.whole_dp
    fan_ef_raw = c_fan.fan_ef()
    torque = float(data_matrix[-1][0])
    total_volume = data_matrix[1][-1]
    date = time.strftime('%Y/%m/%d', time.localtime(time.time()))

    # start insert data into database
    cursor = conn.cursor()
    insert = """
    INSERT INTO cfd_project(`Project`, `Version`, `File_address`, `Producer`, `Date`, `RPM`, `Torque`, `Fan_efficiency`, 
    `Total_volume`, `Total_pressure_loss`) 
    VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');
    """ % (project_name, version, file_path, producer, date, rpm, torque, fan_ef_raw, total_volume, whole_dp)
    cursor.execute(insert)
    last_id = cursor.lastrowid
    conn.commit()
    cursor.close()

    # insert data into volume table
    percentage = [float(x.replace('%', ''))/100 for x in data_matrix[2]]
    volume = [float(x) for x in data_matrix[1]]
    cursor = conn.cursor()
    for i in range(len(data_matrix[0])):
        volume_table = """INSERT INTO cfd_volume(`Project_id`, `Face_name`, `Volume(L/S)`, `Percentage`) 
        VALUES ('%s', '%s', '%s', '%s');""" % (last_id, data_matrix[0][i], volume[i], percentage[i])
        cursor.execute(volume_table)
    conn.commit()
    cursor.close()

    # insert data into static pressure table
    sp = [float(x) for x in data_matrix[4]]
    cursor = conn.cursor()
    for i in range(len(data_matrix[3])):
        sp_table = """INSERT INTO cfd_sp(`Project_id`, `Face_name`, `Static_pressure`) 
            VALUES ('%s', '%s', '%s');""" % (last_id, data_matrix[3][i], sp[i])
        cursor.execute(sp_table)
    conn.commit()
    cursor.close()

    # insert data into total pressure table
    tp = [float(x) for x in data_matrix[6]]
    cursor = conn.cursor()
    for i in range(len(data_matrix[5])):
        tp_table = """INSERT INTO cfd_tp(`Project_id`, `Face_name`, `Total_pressure`) 
               VALUES ('%s', '%s', '%s');""" % (last_id, data_matrix[5][i], tp[i])
        cursor.execute(tp_table)
    conn.commit()
    cursor.close()

    # insert data into total pressure table
    uni = [float(x) for x in data_matrix[8]]
    cursor = conn.cursor()
    for i in range(len(data_matrix[7])):
        tp_table = """INSERT INTO cfd_uni(`Project_id`, `Face_name`, `Uniformity`) 
                   VALUES ('%s', '%s', '%s');""" % (last_id, data_matrix[7][i], uni[i])
        cursor.execute(tp_table)
    conn.commit()
    cursor.close()


insert_data(conn, data_matrix, project_name, version, new_path, producer, rpm)


def extract_data(conn, project_name, version):
    # search main table
    cursor = conn.cursor(pymysql.cursors.DictCursor)   # return Dictionary_like key_valve
    serh = """
    SELECT  * FROM cfd_project where Project = '%s' and Version = '%s'
    """ % (project_name, version)
    cursor.execute(serh)
    data = cursor.fetchone()
    print('main table data:', data)
    cursor.close()

    # search volume table
    ID = data['ID']
    cursor = conn.cursor()
    s_volume = """
    SELECT `Face_name`, `Volume(L/S)`, `Percentage` FROM cfd_volume where Project_id = '%s'
    """ % (ID)
    cursor.execute(s_volume)
    volume_data = cursor.fetchall()
    print(volume_data)
    cursor.close()

    # search sp table
    cursor = conn.cursor()
    s_sp = """
        SELECT `Face_name`, `Static_pressure` FROM cfd_sp where Project_id = '%s'
        """ % (ID)
    cursor.execute(s_sp)
    sp_data = cursor.fetchall()
    print(sp_data)
    cursor.close()

    # search tp table
    cursor = conn.cursor()
    s_tp = """
        SELECT `Face_name`, `Total_pressure` FROM cfd_tp where Project_id = '%s'
        """ % (ID)
    cursor.execute(s_tp)
    tp_data = cursor.fetchall()
    print(tp_data)
    cursor.close()

    # search uni table
    cursor = conn.cursor()
    s_uni = """
            SELECT `Face_name`, `Uniformity` FROM cfd_uni where Project_id = '%s'
            """ % (ID)
    cursor.execute(s_uni)
    uni_data = cursor.fetchall()
    print('This is uni data:', uni_data)
    cursor.close()

    return data


# data = extract_data(conn, project_name, version)
conn.close()
