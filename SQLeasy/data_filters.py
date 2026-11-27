
def normalize_text(value):
  """Limpia un valor de texto y lo devuelve en minúsculas sin espacios extremos; si es nulo o queda vacío, devuelve None."""
  if value is None:
    return None
  cleaned = str(value).strip().lower()
  return cleaned if cleaned else None

def normalize_email(value):
  """
  Normaliza un correo y devuelve None si es nulo, vacío o un marcador no válido.
  """
  cleaned = normalize_text(value)
  if cleaned is None or cleaned in INVALID_EMAIL_MARKERS:
    return None
  return cleaned

def find_duplicates(candidates, existing_rows):
  """
  Compara las tuplas candidatas (sin id) frente a filas existentes (id, name, email) y devuelve coincidencias estructuradas.
  """
  if not candidates or not existing_rows:
    return []

  normalized_existing = []
  for row in existing_rows:
    if not row or len(row) < 3:
      continue
    row_id, row_name, row_email = row[0], row[1], row[2]
    normalized_existing.append({
      "id": row_id,
      "raw_name": row_name,
      "raw_email": row_email,
      "norm_name": normalize_text(row_name),
      "norm_email": normalize_email(row_email),
    })

  matches = []
  for item in candidates:
    if not item or len(item) <= 5:
      continue
  
    raw_name = item[0]
    raw_email = item[5]
    cand_name = normalize_text(raw_name)
    cand_email = normalize_email(raw_email)

    for existing in normalized_existing:
      name_match = (
        cand_name is not None and cand_name == existing["norm_name"]
      )
      email_match = (
        cand_email is not None and cand_email == existing["norm_email"]
      )

      if not (name_match or email_match):
        continue

      if name_match and email_match:
        reason = "nombre y email"
      elif name_match:
        reason = "nombre"
      else:
        reason = "email"

      matches.append({
        "candidate_name": raw_name,
        "candidate_email": raw_email,
        "existing_id": existing["id"],
        "existing_name": existing["raw_name"],
        "existing_email": existing["raw_email"],
        "reason": reason,
      })

  return matches

def format_matches(matches):
  """
  Formatea la lista de coincidencias estructuradas en líneas legibles o devuelve un mensaje si está vacía.
  """
  if not matches:
    return ["Sin coincidencias detectadas."]

  formatted_lines = []
  for match in matches:
    line = (
      f"{match['candidate_name']} -> coincide con -> "
      f"({match['existing_id']}) {match['existing_name']} "
      f"| motivo: {match['reason']} "
      f"| email_candidato: {match['candidate_email']} "
      f"| email_existente: {match['existing_email']}"
    )
    formatted_lines.append(line)

  return formatted_lines

def write_matches_log(formatted_lines, file_name):
  """
  Escribe las líneas formateadas en un archivo de log y avisa por consola.
  """
  with open(file_name, "a", encoding="UTF-8") as log_file:
    for line in formatted_lines:
      log_file.write(f"{line}\n")

  print(f"Puede consultar el log en {file_name}")
  return file_name

def check_dummy_duplicates(file_name="duplicates.log"):
  """
  Consulta registros existentes con start_query, detecta duplicados y vuelca el resultado al log.
  """
  
  from data_ops import start_query
  
  existing_rows = start_query(sql_strings.repeated_names)
  matches = find_duplicates(sql_strings.val, existing_rows)
  formatted_lines = format_matches(matches)
  return write_matches_log(formatted_lines, file_name=file_name)