import re
import datetime

# Valide un nom de 2 à 50 caractères
def is_name(value):
    return 2 <= len(value) <= 50 and all(c.isalpha() or c.isspace() for c in value)

# Valide une date au format YYYY-MM-JJ
def is_date(value):
    try:
        datetime.date.fromisoformat(value)
        return True
    except (ValueError, TypeError):
        return False

# Valide un numéro de téléphone guinéen au format +224 6xx xxx xxx
def is_phone(value):
    # L'expression régulière a été mise à jour pour le format guinéen.
    # Elle accepte l'indicatif +224, suivi de 9 chiffres.
    return re.fullmatch(r"^\+224\s?\d{9}$", value) is not None

# Valide une adresse email simple
def is_email(value):
    return re.fullmatch(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", value) is not None