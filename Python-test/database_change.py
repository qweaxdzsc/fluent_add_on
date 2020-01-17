import pymysql
import time


user_name = 'root'
pwd = 'Sdaac=12345'

conn = pymysql.connect(host='localhost',
                       user=user_name,
                       password=pwd,
                       db='cfd-result',
                       charset='utf8mb4'
                    )

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


def update_whole_data(conn, update_field):
    # search main table
    cursor = conn.cursor()   # return Dictionary_like key_valve
    serh = """
    SELECT %s FROM cfd_project
    """ % (update_field)
    cursor.execute(serh)
    data = cursor.fetchall()
    print('main table data:', data)
    # update
    for i in data:
        update = """
        update `cfd-result`.`cfd_project` set File_address = replace(File_address, 'G:\\\\111', "G:\\\\") 
        where `ID` = %s;
        """ % (i[0])
        cursor.execute(update)
    conn.commit()
    # update
    cursor.close()


if __name__ == "__main__":
    start_time = time.time()
    update_whole_data(conn, 'ID')
    conn.close()
    end_time = time.time()
    print('time cost', end_time - start_time, 's')
