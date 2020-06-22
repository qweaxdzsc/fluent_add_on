import os
import cgitb


class output_web():
    def __init__(self, output_path, data_dict):
        self.output_path = output_path
        self.d = data_dict
        # --------init variable--------
        self.html = ''
        self.title = ''
        self.RPM_table = ''
        self.porous_table = ''
        self.outlet_k_table = ''
        self.valve_table = ''
        self.comment = ''
        # --------start process---------
        self.set_all_data()
        self.form_html()
        self.output()

    def form_html(self):
        self.html = """
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
                     
                <div style="margin-left:120px;margin-right:120px">
                     <div class="lineblock"></div>
                     <div>%s</div>
                     
                     <div class="lineblock"></div>
                     <div>%s</div>
                     
                     <div class="lineblock"></div>
                     <div>%s</div>
                     
                     <div class="lineblock"></div>
                     <div>%s</div>
                     
                     <div class="lineblock"></div>
                     <div>%s</div>

                </div>
                </body>
                </html>""" % (
                                self.title,
                                self.RPM_table,
                                self.porous_table,
                                self.outlet_k_table,
                                self.valve_table,
                                self.comment
                                )

    def regular_table(self, data_dict, head):
        """form html table tag"""
        # table head line
        th_txt = ''
        for i in head:
            th_txt += '<th scope="col">%s</th>\n' % i
        # table tag base
        table = """                                                 
        <table class="hor-zebra">
            <thead>
                <tr>
                    %s
                </tr>
            </thead>
            <tbody>""" % th_txt
        modes = list(data_dict.keys())
        for mode in range(len(modes)):                              # get how many lines
            if mode % 2 == 0:                                          # add color for odd line
                color_bar = 'class="odd"'
            else:
                color_bar = ''
            table += '\n<tr %s>' % color_bar
            table += '\n<td>%s</td>' % (modes[mode])                       # add data for row
            table += '\n<td>%s</td>' % (data_dict[modes[mode]])
            table += '\n</tr>'

        table += '\n</tbody>'+'\n</table>'                          # finish table
    
        return table

    def get_porous_table(self, data_dict, head):
        """form html table tag"""
        # table head line
        th_txt = ''
        for i in head:
            th_txt += '<th scope="col">%s</th>\n' % i
        # table tag base
        table = """                                                 
                <table class="hor-zebra">
                    <thead>
                        <tr>
                            %s
                        </tr>
                    </thead>
                    <tbody>""" % th_txt

        table += '\n<tr class="odd">'
        table += '\n<td>Evaporator</td>'
        table += '\n<td>%s</td>' % (data_dict['evap'])            # add data for row
        table += '\n<td>%s</td>' % (data_dict['evap_c1'])
        table += '\n<td>%s</td>' % (data_dict['evap_c2'])
        table += '\n</tr>'
        table += '\n<tr>'
        table += '\n<td>Heater</td>'
        table += '\n<td>%s</td>' % (data_dict['hc'])  # add data for row
        table += '\n<td>%s</td>' % (data_dict['hc_c1'])
        table += '\n<td>%s</td>' % (data_dict['hc_c2'])
        table += '\n</tr>'
        table += '\n<tr class="odd">'
        table += '\n<td>Filter</td>'
        table += '\n<td>%s</td>' % (data_dict['filter'])  # add data for row
        table += '\n<td>%s</td>' % (data_dict['filter_c1'])
        table += '\n<td>%s</td>' % (data_dict['filter_c2'])
        table += '\n</tr>'
        table += '\n</tbody>' + '\n</table>'                    # finish table

        return table

    def comment_div(self, data_dict):
        div = """<div style="font-size: 20px;
                            font-weight: normal;
                            text-align: left;
                            padding: 10px 8px;
                            color: #039;">Comment</div>"""
        div += """<div style="text-align: left;
                            padding: 5px 8px;
                            color: #000;">%s
                            </div>""" % data_dict['comment']

        return div

    def set_all_data(self):
        self.title = self.d['project_name']
        self.RPM_table = self.regular_table(self.d['RPM'], ['Mode', 'RPM'])
        self.porous_table = self.get_porous_table(self.d['porous'], ['Porous', 'name', 'C1', 'C2'])
        self.outlet_k_table = self.regular_table(self.d['outlet_k'], ['Outlet', 'K'])
        self.valve_table = self.regular_table(self.d['valve'], ['Valve', 'Angle'])
        self.comment = self.comment_div(self.d['comment'])

    def output(self):
        report = open(self.output_path, 'w')
        report.write(self.html)
        report.close()
        os.system(r'"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" %s' % self.output_path)


cgitb.enable(format='text')