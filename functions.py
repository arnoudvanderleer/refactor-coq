import os

def get_source_files(directory):
  return [
    (path, file)
    for (path, subdirs, files) in os.walk(directory)
    for file in files
    if file.split(".")[-1] == "v"
  ]

def get_namespace(path, name):
  name = ".".join(name.split(".")[:-1])
  return os.path.join(path, name).replace("/", ".")

def get_glob_lines(glob_root, path, name):
  glob_name = ".".join([*name.split(".")[:-1], "glob"])
  filename = os.path.join(glob_root, path, glob_name)
  with open(filename, "r") as f:
    return [line[:-1].split() for line in set(f.readlines())]

def get_definitions(kinds, lines):
  return [
    (int(line[1].split(":")[1]) + 1, line[3])
    for line in lines
    if line[0] in kinds
  ]

def get_references(lines):
  return [
    (int(line[0].split(":")[1]) + 1, line[1], line[3])
    for line in lines
    if line[0][0] == "R"
  ]
