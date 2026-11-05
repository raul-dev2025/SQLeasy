import os
import SQLeasy_psg as SQLeasy

def counter_iterator(x):
  while True:
    yield x
    x = x + 1


def list_fn(n=1):
  path = os.path.dirname(__file__)
  file_path = os.path.join(path, 'modAttr.py')
  with open(file_path, mode="w", encoding="utf-8") as file:
    functions = dir(SQLeasy)
    counter = counter_iterator(n)
    for fn in functions:
      file.write('{} {}()\n'.format(next(counter), fn))


def display_options():
  """
  This is the documentation for the display_options function.
  """
  path = os.path.dirname(__file__)
  file_path = os.path.join(path, 'modAttr.py')
  
  # Si el archivo de opciones no existe, lo generamos al vuelo
  if not os.path.exists(file_path):
    list_fn(1)

  a_list = []
  with open(file_path, mode="r", encoding="utf-8") as pattern_file:
    for line in pattern_file:
      string = line.split(None, 2)
      if len(string) >= 2:
        a_list.append((string[0], string[1]))
        # Imprimimos la opción en pantalla para que el usuario la vea
        # print(f"\t{string[0]} - {string[1]}")

  result = dict(a_list)
  return result