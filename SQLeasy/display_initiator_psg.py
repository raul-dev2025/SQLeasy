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

def dump_html_styled(target_file='dump.html'):
    '''
    Lee el archivo dump.html generado por Pandas, aplica la estructura
    HTML5 completa, enlaza la hoja de estilos css/tablas.css y asigna las 
    clases .custom-table y .custom-table-container.
    '''
    if not os.path.exists(target_file):
        return

    with open(target_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Reemplazar la etiqueta de tabla por la versión con las clases de estilo
    old_tag = '<table border="1" class="dataframe">'
    new_tag = '<table border="1" class="dataframe custom-table custom-table-container">'
    
    if old_tag in content:
        content = content.replace(old_tag, new_tag)
    else:
        content = content.replace('<table', '<table class="custom-table custom-table-container"')

    # Envolver en la estructura HTML completa vinculando la hoja de estilos externa
    full_html = f'''<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <link rel="stylesheet" href="css/tablas.css">
</head>
<body>
{content}
</body>
</html>'''

    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(full_html)

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