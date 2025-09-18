#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def validate_email(email):
    """Valide une adresse email"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    """Valide un numéro de téléphone"""
    import re
    pattern = r'^[0-9+\-\s()]{10,}$'
    return re.match(pattern, phone) is not None

def validate_name(name):
    """Valide un nom"""
    return len(name.strip()) >= 2 and name.replace(' ', '').isalpha()

def validate_date(date_str):
    """Valide une date"""
    try:
        from datetime import datetime
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except:
        return False
