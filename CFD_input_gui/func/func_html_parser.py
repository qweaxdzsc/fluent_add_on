class HtmlParser(object):
    """what is it:
    It is special html parser to extract data from input_ui's html parameter file
    how it works:
    1. read it as txt in
    2. divide it into different parts by different data class
    3. extract data from each part to different dicts
    4. form all dicts to one result dict"""
    def __init__(self, html_path):
        self.html_path = html_path
        # ------- init variable--------
        self.html = ''
        self.body_html = ''
        self.project_name = ''
        self.RPM_div = ''
        self.porous_div = ''
        self.outlet_k_div = ''
        self.valve_div = ''
        self.comment = ''
        self.data_dict = {}
        self.RPM_dict = {}
        self.porous_dict = {}
        self.outlet_k_dict = {}
        self.valve_dict = {}
        # ------- process --------------
        self.process_html()

    def process_html(self):
        self.pre_parser()
        self.get_title()
        # ------------- divide into divs ----------
        self.RPM_div = self.divide_div('RPM')
        self.porous_div = self.divide_div('Porous')
        self.outlet_k_div = self.divide_div('Outlet')
        self.valve_div = self.divide_div('Valve')
        # ------------- form dict -----------------
        self.RPM_dict = self.easy_dict(self.RPM_div, self.RPM_dict)
        self.valve_dict = self.easy_dict(self.valve_div, self.valve_dict)
        self.outlet_k_dict = self.easy_dict(self.outlet_k_div, self.outlet_k_dict)
        self.get_porous_dict()
        self.get_comment()
        self.form_data_dict()

    def pre_parser(self):
        with open(self.html_path, 'r') as f:
            self.html = f.readlines()
            row_number = len(self.html)
            for i in range(row_number):
                self.html[i] = self.html[i].strip()

    def get_title(self):
        for row in self.html:
            if 'h2' in row:
                self.project_name = row[43:-5]                          # use specific index to get project_name
                row_index = self.html.index(row)
                self.html = self.html[row_index+1:]
                self.body_html = self.html
                break

    def divide_div(self, head_marker):
        """Sequentially divide html into divs"""
        div = None
        for row in self.html:
            if head_marker in row:
                head_index = self.html.index(row)
                self.html = self.html[head_index + 1:]
                for i in self.html:
                    if 'class="lineblock"' in i:
                        end_index = self.html.index(i)
                        div = self.html[:end_index]
                        self.html = self.html[end_index:]
                        break
                break

        return div

    def get_comment(self):
        for row in self.html:
            if 'color: #000;">' in row:
                self.comment = row[14:]                                 # use specific index to divide row and get text

    def easy_dict(self, div, dict):
        for row in div:
            if '<tr' in row:
                row_index = div.index(row)
                name_row = div[row_index + 1]
                name = name_row[4:-5]
                value_row = div[row_index + 2]
                value = value_row[4:-5]
                dict[name] = value
                div = div[row_index+2:]
        
        return dict

    def get_porous_dict(self):
        for row in self.porous_div:
            if 'Evaporator' in row:
                evap_row = self.porous_div.index(row)
                self.porous_dict['evap'] = self.porous_div[evap_row+1][4:-5]
                self.porous_dict['evap_c1'] = self.porous_div[evap_row + 2][4:-5]
                self.porous_dict['evap_c2'] = self.porous_div[evap_row + 3][4:-5]
            if 'Heater' in row:
                hc_row = self.porous_div.index(row)
                self.porous_dict['hc'] = self.porous_div[hc_row + 1][4:-5]
                self.porous_dict['hc_c1'] = self.porous_div[hc_row + 2][4:-5]
                self.porous_dict['hc_c2'] = self.porous_div[hc_row + 3][4:-5]
            if 'Filter' in row:
                filter_row = self.porous_div.index(row)
                self.porous_dict['filter'] = self.porous_div[filter_row + 1][4:-5]
                self.porous_dict['filter_c1'] = self.porous_div[filter_row + 2][4:-5]
                self.porous_dict['filter_c2'] = self.porous_div[filter_row + 3][4:-5]

    def form_data_dict(self):
        self.data_dict['project_name'] = self.project_name
        self.data_dict['RPM'] = self.RPM_dict
        self.data_dict['porous'] = self.porous_dict
        self.data_dict['outlet_k'] = self.outlet_k_dict
        self.data_dict['valve'] = self.valve_dict
        self.data_dict['comment'] = self.comment


if __name__ == "__main__":
    html_path = r'C:/Users/BZMBN4/Desktop/123.html'
    project_info = HtmlParser(html_path)
    print(project_info.data_dict)

