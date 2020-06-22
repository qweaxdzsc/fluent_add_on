import csv

csv_path = r'C:\Users\BZMBN4\Desktop\123.csv'
data_dict = dict()

with open(csv_path, 'r') as csvfile:
    reader = csv.reader(csvfile)
    print(reader)
    for row in reader:
        try:
            sub_dict = eval(row[1])
        except Exception as e:
            data_dict[row[0]] = row[1]
        else:
            data_dict[row[0]] = sub_dict
