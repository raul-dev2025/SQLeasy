
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

  


  return matches
