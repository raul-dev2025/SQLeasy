sql = """
  INSERT INTO teacher (teacher_id, first_name, last_name, language_1, language_2, dob, tax_id, phone_no)
  VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
"""

deafult_val = [
    (7, 'Hunk', 'Dodson', 'ENG', None, '1991-12-23', 11111, '+09812734098'),
    (8, 'Funk', 'Bolson', 'EKR', 'ENG', '1491-15-16', 22222, '+09219014098')
]