import sys
sys.path.append('src')
from database.connection import get_db_connection

print('🗑️ Suppression de toutes les données des professeurs...')
conn = get_db_connection()
cursor = conn.cursor()

try:
    # Supprimer toutes les contraintes de clé étrangère
    cursor.execute('''
        DECLARE @sql NVARCHAR(MAX) = '';
        SELECT @sql = @sql + 'ALTER TABLE ' + OBJECT_NAME(parent_object_id) + ' DROP CONSTRAINT ' + name + ';'
        FROM sys.foreign_keys 
        WHERE referenced_object_id = OBJECT_ID('professeurs');
        EXEC sp_executesql @sql;
    ''')
    print('✅ Contraintes de clé étrangère supprimées')
    
    # Supprimer la table professeurs complètement
    cursor.execute('DROP TABLE professeurs')
    print('✅ Table professeurs supprimée')
    
    # Supprimer les références dans la table cours
    cursor.execute('UPDATE cours SET professeur_id = NULL')
    print('✅ Références dans cours supprimées')
    
    conn.commit()
    print('🎉 Toutes les données des professeurs supprimées !')
    
except Exception as e:
    print(f'❌ Erreur: {e}')
finally:
    conn.close()
