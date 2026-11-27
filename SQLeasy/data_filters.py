
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

  


  return matches
