
project_name = 'GE2-rear2'
version = 'V7-FC'


def get_ppt(project_name, version):

    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    import time
    import os
    import numpy as np
    from pptx.enum.text import MSO_ANCHOR
    from pptx.enum.text import PP_ALIGN
    import pymysql

    # extract info from mysql
    user_name = 'root'
    pwd = 'Sdaac=12345'

    conn = pymysql.connect(host='localhost',
                           user=user_name,
                           password=pwd,
                           db='cfd-result',
                           charset='utf8mb4'
                           )


    # search main table
    cursor = conn.cursor(pymysql.cursors.DictCursor)  # return Dictionary_like key_valve
    serh = """
    SELECT  * FROM cfd_project where Project = '%s' and Version = '%s'
    """ % (project_name, version)
    cursor.execute(serh)
    main_data = cursor.fetchone()
    print('main table data:', main_data)
    cursor.close()

    # search volume table
    ID = main_data['ID']
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
            SELECT `Uniformity` FROM cfd_uni where Project_id = '%s' and Face_name = '%s'
            """ % (ID, 'evap_out')
    cursor.execute(s_uni)
    uni_data = cursor.fetchone()
    print('This is uni data:', uni_data)
    cursor.close()
    conn.close()

    # info process
    result_path = main_data['File_address']
    RPM = str(main_data['RPM'])
    total_volume = str(main_data['Total_volume'])
    volume_data = [list(x) for x in volume_data]
    torque = str(main_data['Torque'])
    fan_efficiency = '%.1f %%'% (main_data['Fan_efficiency']*100)

    whole_title = project_name + '-' + version
    evap_out_uni = str(uni_data[0])


    # start PPT writing
    ppt = Presentation(r'C:\Users\BZMBN4\Documents\Custom Office Templates\test.pptx')  # call template

    def cover_slide(title):
        cover_slide = ppt.slides[0]
        title_shape = cover_slide.shapes.placeholders[0]
        title_shape.text_frame.clear()
        p = title_shape.text_frame.paragraphs[0]
        run1 = p.add_run()
        run1.text = '%s\nCFD result\n\n' %(title)
        run1.font.name = 'Arial Unicode MS'
        run1.font.size = Pt(36)
        run1.font.italic = True
        run1.font.color.rgb = RGBColor(255, 255, 255)

        run2 = p.add_run()
        run2.text = time.strftime('%Y/%m/%d', time.localtime(time.time()))
        run2.font.name = 'Calibri Light'
        run2.font.size = Pt(40)
        run2.font.italic = True
        run2.font.color.rgb = RGBColor(255, 255, 255)


    def title_set(slide, title_name):
        title = slide.shapes[0].text_frame.paragraphs[0]
        title.text = '%s' %(title_name)
        title.font.name = 'Arial Unicode MS'
        title.font.size = Pt(28)
        title.font.color.rgb = RGBColor(46, 117, 182)


    def place_table(row, col, left, top, width, height, slide):

        table = slide.shapes.add_table(row, col, left, top, width, height).table     # create table
        for j in range(row):                                                         # change color for table
            if j == 0:
                for i in range(col):
                    table.cell(0, i).fill.solid()
                    table.cell(0, i).fill.fore_color.rgb = RGBColor(68, 114, 196)
            elif j % 2 == 0 and j > 0:
                for i in range(col):
                    table.cell(j, i).fill.solid()
                    table.cell(j, i).fill.fore_color.rgb = RGBColor(233, 235, 245)
            else:
                for i in range(col):
                    table.cell(j, i).fill.solid()
                    table.cell(j, i).fill.fore_color.rgb = RGBColor(207, 213, 234)
        return table


    # create cover slide
    cover_slide(project_name)

    # create overview slide
    overview_slide = ppt.slides[1]
    title_set(overview_slide, project_name+'-' + version + '-CFD-Result')

    col = 7                                             # create table
    row = 2
    left = Inches((1+(7-col)*0.4)/2)
    top = Inches(2.2-row*0.1)
    width = Inches(9-(7-col)*0.4)
    height = Inches(0.8*row)
    ov_table = place_table(row, col, left, top, width, height, overview_slide)


    # input data
    heading = ['Project', 'Version', 'RPM', 'Volume\n(L/S)', 'Uniformity\nEvap_out', 'Torque\n(N*M)', 'Fan\nefficiency']
    for i in range(col):
        ov_table.cell(0, i).text = heading[i]

    ov_table.cell(1, 0).text = project_name
    ov_table.cell(1, 1).text = version
    ov_table.cell(1, 2).text = RPM
    ov_table.cell(1, 3).text = total_volume
    ov_table.cell(1, 4).text = evap_out_uni
    ov_table.cell(1, 5).text = torque
    ov_table.cell(1, 6).text = fan_efficiency


    # aligning center the table text
    def aligning_table(table):
        row = len(table.rows)
        col = len(table.columns)
        lenth_matrix = np.zeros([row, col])
        for i in range(row):
            for j in range(col):
                table.cell(i, j).vertical_anchor = MSO_ANCHOR.MIDDLE                     # vertical center alignment
                for k in range(len(table.cell(i, j).text_frame.paragraphs)):
                    table.cell(i, j).text_frame.paragraphs[k].alignment = PP_ALIGN.CENTER    # horizontal center alignment
                lenth_matrix[i, j] = len(table.cell(i, j).text)

        return lenth_matrix


    def auto_wid_table(col, lenth_matrix, table):
        str_wid = np.zeros(col)
        total_wid = 0
        for i in range(col):                                                                   # table auto-width
            str_wid[i] = max(lenth_matrix[:, i])*3 + 62
            table.columns[i].width = Pt(str_wid[i])
            total_wid += str_wid[i]


    word_lenth = aligning_table(ov_table)
    auto_wid_table(col, word_lenth, ov_table)

    # create distribution slide
    dis_slide = ppt.slides[2]
    print(len(dis_slide.shapes))
    title_set(dis_slide, whole_title + '-distribution')

    col = 3                                                     # place table
    row = len(volume_data) + 1
    left = Inches((2+(7-col)*0.4)/2)
    top = Inches(3.2-row*0.1)
    width = Inches(8-(7-col)*0.4)
    height = Inches(0.5*row)
    dis_table = place_table(row, col, left, top, width, height, dis_slide)

    # put data in
    dis_table_head = ['', 'Volume(L/S)', 'Percentage(%)']
    for i in range(len(dis_table_head)):
        dis_table.cell(0, i).text = dis_table_head[i]

    for i in range(row-1):
        for j in range(len(volume_data[0])):
            if j == 2:
                volume_data[i][j] = '%.1f%%' % (((volume_data[i][j]))*100)
            dis_table.cell(i+1, j).text = str(volume_data[i][j])


    # modify font in table
    def table_font(table, head_size, body_size):
        for i in range(row):
            if i == 0:
                for j in range(col):
                    table.cell(0, j).text_frame.paragraphs[0].font.size = head_size
            else:
                for j in range(col):
                    table.cell(i, j).text_frame.paragraphs[0].font.size = body_size
                    table.cell(i, j).text_frame.paragraphs[0].font.bold = True


    table_font(dis_table, Pt(16), Pt(14))
    aligning_table(dis_table)

    # streamline slide
    strm_slide = ppt.slides[3]
    title_set(strm_slide, whole_title + '-Streamline')

    # streamline table
    strm_table = strm_slide.shapes[2].table


    def jpg_table_head(table, heading):
        table.cell(0, 0).text = heading[0]
        table.cell(0, 0).text_frame.paragraphs[0].font.color.rgb = RGBColor(0, 0, 0)
        table.cell(0, 0).text_frame.paragraphs[0].font.bold = False

        table.cell(1, 0).text = heading[1]
        table.cell(1, 0).text_frame.paragraphs[0].font.color.rgb = RGBColor(0, 0, 0)
        table.cell(1, 0).text_frame.paragraphs[0].font.bold = False


    strm_table_head = ['Whole_pathline', 'Distrib_pathline']
    jpg_table_head(strm_table, strm_table_head)


    def jpg_into_table(result_path, slide, first_picture, second_picture):

        file_path = result_path + '\\'

        left = Inches(3.5)
        top = Inches(1.2)
        width = Inches(4.6)
        slide.shapes.add_picture(file_path + first_picture, left, top, width)

        left = Inches(3.5)
        top = Inches(4.2)
        width = Inches(4.6)
        slide.shapes.add_picture(file_path + second_picture, left, top, width)


    jpg_into_table(result_path, strm_slide, 'whole_pathline.jpg', 'distrib_pathline.jpg')

    # contour slide

    cont_slide = ppt.slides[4]
    title_set(cont_slide, whole_title + '-Evap_out-Contour')
    cont_table = cont_slide.shapes[2].table

    cont_table_head = ['Evap_out Contour', 'Evap_out_0-4 Contour']
    jpg_table_head(cont_table, cont_table_head)
    jpg_into_table(result_path, cont_slide, 'evap_out.jpg', 'evap_out.jpg')

    # Pressure Drop slide

    dp_slide = ppt.slides[5]
    title_set(dp_slide, whole_title + '-Pressure-Drop')

    col = 2                                             # create table
    row = len(sp_data) + 1
    left = Inches(1)
    top = Inches(1.5)
    width = Inches(3.5)
    height = Inches(0.6*row)
    sp_table = place_table(row, col, left, top, width, height, dp_slide)

    sp_table_head = ['Static Pressure', version]


    def dp_table_create(table, head, dp_data):
        for j in range(col):
            table.cell(0, j).text = head[j]

        for i in range(row-1):
            for j in range(len(dp_data[0])):
                table.cell(i+1, j).text = str(dp_data[i][j])

        table_font(table, Pt(16), Pt(14))
        aligning_table(table)


    dp_table_create(sp_table, sp_table_head, sp_data)


    tp_table = place_table(row, col, Inches(5), top, width, height, dp_slide)
    tp_table_head = ['Total Pressure', version]

    dp_table_create(tp_table, tp_table_head, tp_data)


    # save ppt and open it
    ppt.save(result_path +'\\' +whole_title+ '.pptx')          # save
    os.system(result_path +'\\'+ whole_title + '.pptx')         # open


get_ppt(project_name, version)