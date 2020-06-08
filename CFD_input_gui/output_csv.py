import csv


def OutputCsv(csv_path, data_dict):
    print('start')
    print(csv_path)
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        for i in data_dict.keys():
            writer.writerow([i, data_dict[i]])

    print('finish')


# path = QFileDialog.getSaveFileName(filter='html, *.html')