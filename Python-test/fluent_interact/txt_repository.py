import os

homedir = os.getcwd()


def default():
    with open('repository.txt', "r") as rp:
        info = rp.readlines()
    for line in info:
        line = line.split()

    return line


def write(model, cores):
    if 'm' in model:
        model = 'mesh'
    elif 's' in model:
        model = 'solver'
    new_txt = open(homedir+'\\repository.txt', 'w')
    new_txt.writelines([model, ' ', cores])
    new_txt.close()