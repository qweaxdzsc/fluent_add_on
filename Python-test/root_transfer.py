def add_slash(path):
    path.replace('\\', '\\\\')
    new_path = path + '\\'

    return new_path
