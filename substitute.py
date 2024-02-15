#! /usr/bin/python3

import os
import sys
from functions import get_source_files, get_namespace, get_glob_lines, get_references, get_definitions

def substitute_lines(lines, substitutions, filename):
  tmp_filename = "./tmp.v"
  with open(filename, "rb") as input_file:
    with open(tmp_filename, "w+b") as output_file:
      last_position = 0

      for (end, source, target) in sorted(lines):
        start = end - len(str.encode(source))
        output_file.write(input_file.read(start - last_position))
        output_file.write(str.encode(target))
        input_file.read(end - start)
        last_position = end
      output_file.write(input_file.read())

  os.replace(tmp_filename, filename)

def substitute_file(kinds, substitutions, glob_root, path, name):
  filename = os.path.join(path, name)
  namespace = get_namespace(path, name)

  lines = get_glob_lines(glob_root, path, name)

  lines = [
    (end, src, substitutions[(ns, src)])
    for (end, ns, src) in get_references(lines)
    if (ns, src) in substitutions
  ] + [
    (end, src, substitutions[(namespace, src)])
    for (end, src) in get_definitions(kinds, lines)
    if (namespace, src) in substitutions
  ]

  if len(lines) == 0:
    return

  substitute_lines(lines, substitutions, filename)

def substitute(kinds, substitutions, search_dir, project_root, glob_root):
  old_dir = os.getcwd()
  os.chdir(project_root)

  for path, name in get_source_files(search_dir):
    substitute_file(kinds, substitutions, glob_root, path, name)

  os.chdir(old_dir)

with open("changes.txt", "r+") as input_file:
  lines = [line.strip().split(" ") for line in input_file.readlines()]

substitute(
  ["def", "coe", "prf", "thm"],
  {(line[0], line[2]): line[1] for line in lines},
  sys.argv[1] if len(sys.argv) > 1 else ".",
  sys.argv[2] if len(sys.argv) > 2 else ".",
  sys.argv[3] if len(sys.argv) > 3 else "_build/default",
)
