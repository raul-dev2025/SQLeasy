
def normalize_text(value):
  """Limpia un valor de texto y lo devuelve en minúsculas sin espacios extremos; si es nulo o queda vacío, devuelve None."""
  if value is None:
    return None
  cleaned = str(value).strip().lower()
  return cleaned if cleaned else None
