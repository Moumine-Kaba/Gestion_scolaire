# -*- coding: utf-8 -*-
"""
Script pour corriger les problèmes d'encodage
"""

import os
import re

def fix_encoding_in_file(file_path):
    """Corrige les problèmes d'encodage dans un fichier"""
    print(f"Correction du fichier: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remplacer les emojis par du texte
        replacements = {
            '✅': 'SUCCES -',
            '❌': 'ERREUR -',
            '🚀': '',
            '💰': '',
            '🔍': '',
            '⚡': '',
            '➕': '',
            '📊': '',
            '🎓': '',
            '📋': '',
            '🔄': '',
            '⚙️': '',
            '👁️': '',
            '🔔': '',
            '📈': '',
            '📉': '',
            '💡': '',
            '⚠️': 'ATTENTION -',
            '🗑️': '',
            '🎯': '',
            '📝': '',
            '🔧': '',
            '💾': '',
            '📤': '',
            '📥': '',
            '🎨': '',
            '🌟': '',
            '🔥': '',
            '💯': '',
            '🎉': '',
            '📱': '',
            '💻': '',
            '🖥️': '',
            '⌨️': '',
            '🖱️': '',
            '📊': '',
            '📈': '',
            '📉': '',
            '📋': '',
            '📄': '',
            '📑': '',
            '📜': '',
            '📰': '',
            '📓': '',
            '📔': '',
            '📕': '',
            '📖': '',
            '📗': '',
            '📘': '',
            '📙': '',
            '📚': '',
            '📛': '',
            '📜': '',
            '📝': '',
            '📞': '',
            '📟': '',
            '📠': '',
            '📡': '',
            '📢': '',
            '📣': '',
            '📤': '',
            '📥': '',
            '📦': '',
            '📧': '',
            '📨': '',
            '📩': '',
            '📪': '',
            '📫': '',
            '📬': '',
            '📭': '',
            '📮': '',
            '📯': '',
            '📰': '',
            '📱': '',
            '📲': '',
            '📳': '',
            '📴': '',
            '📵': '',
            '📶': '',
            '📷': '',
            '📸': '',
            '📹': '',
            '📺': '',
            '📻': '',
            '📼': '',
            '📽️': '',
            '📾': '',
            '📿': '',
            '🔀': '',
            '🔁': '',
            '🔂': '',
            '🔃': '',
            '🔄': '',
            '🔅': '',
            '🔆': '',
            '🔇': '',
            '🔈': '',
            '🔉': '',
            '🔊': '',
            '🔋': '',
            '🔌': '',
            '🔍': '',
            '🔎': '',
            '🔏': '',
            '🔐': '',
            '🔑': '',
            '🔒': '',
            '🔓': '',
            '🔔': '',
            '🔕': '',
            '🔖': '',
            '🔗': '',
            '🔘': '',
            '🔙': '',
            '🔚': '',
            '🔛': '',
            '🔜': '',
            '🔝': '',
            '🔞': '',
            '🔟': '',
            '🔠': '',
            '🔡': '',
            '🔢': '',
            '🔣': '',
            '🔤': '',
            '🔥': '',
            '🔦': '',
            '🔧': '',
            '🔨': '',
            '🔩': '',
            '🔪': '',
            '🔫': '',
            '🔬': '',
            '🔭': '',
            '🔮': '',
            '🔯': '',
            '🔰': '',
            '🔱': '',
            '🔲': '',
            '🔳': '',
            '🔴': '',
            '🔵': '',
            '🔶': '',
            '🔷': '',
            '🔸': '',
            '🔹': '',
            '🔺': '',
            '🔻': '',
            '🔼': '',
            '🔽': '',
            '🕐': '',
            '🕑': '',
            '🕒': '',
            '🕓': '',
            '🕔': '',
            '🕕': '',
            '🕖': '',
            '🕗': '',
            '🕘': '',
            '🕙': '',
            '🕚': '',
            '🕛': '',
            '🕜': '',
            '🕝': '',
            '🕞': '',
            '🕟': '',
            '🕠': '',
            '🕡': '',
            '🕢': '',
            '🕣': '',
            '🕤': '',
            '🕥': '',
            '🕦': '',
            '🕧': '',
        }
        
        for emoji, replacement in replacements.items():
            content = content.replace(emoji, replacement)
        
        # Sauvegarder le fichier
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Fichier corrigé: {file_path}")
        
    except Exception as e:
        print(f"Erreur lors de la correction de {file_path}: {e}")

def main():
    """Fonction principale"""
    files_to_fix = [
        'views/paiements_view.py',
        'controllers/database_schema.py',
        'controllers/enhanced_paiement_controller.py'
    ]
    
    for file_path in files_to_fix:
        if os.path.exists(file_path):
            fix_encoding_in_file(file_path)
        else:
            print(f"Fichier non trouvé: {file_path}")

if __name__ == "__main__":
    main()
