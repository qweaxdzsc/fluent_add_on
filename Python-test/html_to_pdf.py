import pdfkit

input_path = 'G:\\519(706)\\519_vent_150mmfan\\706-vent-v11\\result\\706-vent-v11-150mmfan-3800RPM.html'
output_path = 'G:\\519(706)\\519_vent_150mmfan\\706-vent-v11\\result\\706.pdf'
config = pdfkit.configuration(wkhtmltopdf='F:\\zonghui\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')
options = {'page-size': 'A3', 'encoding': "UTF-8"}


pdfkit.from_file(input_path, output_path, configuration=config, options=options)

