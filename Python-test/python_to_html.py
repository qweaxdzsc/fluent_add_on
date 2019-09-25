# Python_to_Html
def get_html(matrix, title, html_output_path):
    import webbrowser
    import os

    # html_output_path = "C:\\Users\\zonghui\\Desktop\\python\\"
    # title = "519-vent-v10-pp1-150mmfan-3800RPM"

    print(matrix)


    # write html tag for volume data table
    def get_table(table_matrix, head):
        # table head line
        th_txt = ''
        for i in range(len(head)):
            th_txt = th_txt + '<th scope="col">%s</th>\n' % head[i]

        table = """
        <table class="hor-zebra">
            <thead>
                <tr>
                    %s
                </tr>
            </thead>
            <tbody>""" % th_txt

        for i in range(len(table_matrix[0])):  # get how many lines
            if i%2 == 0:
                color_bar = 'class="odd"'
            else:
                color_bar = ''

            table += '\n<tr %s>' % color_bar
            for j in range(len(table_matrix)):
                table += '\n<td>' + table_matrix[j][i] + '</td>'

            table = table + '\n</tr>'

        table = table + '\n</tbody>'+'\n</table>'  # <tr> for line, </td> for cell, finish table

        return table


    # get all table's html table
    volume_table = get_table(matrix[0:3], ['Volume Flow Rate', '(L/S)', 'Percentage%'])
    sp_table = get_table(matrix[3:5], ['Static Pressure', '(Pa)'])
    tp_table = get_table(matrix[5:7], ['Total Pressure', '(Pa)'])
    uni_table = get_table(matrix[7:9], ['Uniformity', ' '])
    moment_table = get_table(matrix[9:10], ['Torque(N/M)'])

    # output to HTML

    os.getcwd()
    os.chdir(html_output_path)
    mydir = os.getcwd()  # get directory
    ResultHtml = html_output_path + title + ".html"
    report = open(ResultHtml, 'w')  # create html

    # main frame for html

    message = """
    <html>
    <head>
        <style type="text/css">
            .hor-zebra
            {
                font-family: "Lucida Sans Unicode", "Lucida Grande", Sans-Serif;
                font-size: 15px;
                
                text-align: left;
                border-collapse: collapse;
            }
            .hor-zebra th
            {
                font-size: 20px;
                font-weight: normal;
                width: 200px;
                padding: 10px 8px;
                color: #039;
            }
            .hor-zebra td
            {
            
                padding: 8px;
                color: #000;
            }
            .hor-zebra .odd
            {
                background: #e8edff; 
            }
            
            
            .lineblock{
                width:90%%;
                height:1.5px;
                margin:30px;
                background:linear-gradient(to left,#efefef,#ADADAD,#efefef);
            }
        </style>
    </head>
    <body>
         <div style="text-align:center;margin-top:20px;margin-bottom:10px">
         <h2 style="font-size:54px;display:inline;">%s</h2>
         
         </div>
         <div style="margin-top:5px;padding:0;text-align:center;">
         <span>File Location: %s </span><span>&nbsp;&nbsp;&nbsp;</span>
         <span> Author: Zonghui.Jin</span>
         </div>
         
         <div class="lineblock"></div>
    
    <body style="margin-left:120px;margin-right:120px" >
        <div summary = volume flow table">%s</div>
        <div class="lineblock"></div>
        <div>%s</div>
        
        <div class="lineblock"></div>
        <div>%s</div>
        
        <div class="lineblock"></div>
        <div>%s</div>
        
        <div class="lineblock"></div>
        <div>%s</div>
        
        <div class="lineblock"></div>
        <h4 style="font-size:30px">Distrib_pathline</h4>
        <img src="distrib_pathline.jpg" width = 900px  />
        
        <div class="lineblock"></div>     
        <h4 style="font-size:30px">Whole_pathline</h4>
        <img src="whole_pathline.jpg" width = 900px />
        
        <div class="lineblock"></div>
        <h4 style="font-size:30px">Evap_out_Contour</h4>   
        <img src="evap_out.jpg" width = 900px />
        
        <div class="lineblock"></div>
        <h4 style="font-size:30px">Evap_out_0-4_Contour</h4>   
        <img src="evap_out_0-4.jpg" width = 900px /> 
        
        <div class="lineblock"></div>
        <h4 style="font-size:30px">Filter_out_Contour</h4>
        <img src="filter_out.jpg" width = 900px />
            
        <div class="lineblock"></div> 
        <h4 style="font-size:30px">Filter_out_0-4_Contour</h4>
        <img src="filter_out_0-4.jpg" width = 900px />
          
        <div class="lineblock"></div>      
        <h4 style="font-size:30px">Hc_out Contour</h4>
        <img src="hc_out.jpg" width = 900px/>      
        
    </body>
    </html>""" % (title, mydir, volume_table, sp_table, tp_table, uni_table, moment_table)

    report.write(message)  # write to html
    report.close()  # close edit
    webbrowser.open(ResultHtml, 1)  # open web

