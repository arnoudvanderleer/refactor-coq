#! /usr/bin/python3

import inflection
import os
import sys
from functions import get_source_files, get_namespace, get_glob_lines, get_definitions

def get_substitutions(kinds, search_dir, project_root, glob_root):
  old_dir = os.getcwd()
  os.chdir(project_root)

  lines = set()

  i = 0
  substitutions = {}

  for path, name in get_source_files(search_dir):
    namespace = get_namespace(path, name)

    definitions = get_definitions(kinds, get_glob_lines(glob_root, path, name))

    for end, name in definitions:
      snake_name = inflection.underscore(name)
      if snake_name == name: continue
      lines.add(f'{namespace} {snake_name} {name}')

  os.chdir(old_dir)

  return sorted(list(set(lines)))

substitutions = get_substitutions(
  ["def", "coe", "prf", "thm"],
  sys.argv[1] if len(sys.argv) > 1 else ".",
  sys.argv[2] if len(sys.argv) > 2 else ".",
  sys.argv[3] if len(sys.argv) > 3 else "_build/default",
)

with open("changes.txt", "w+") as output_file:
  output_file.write("\n".join(substitutions))


