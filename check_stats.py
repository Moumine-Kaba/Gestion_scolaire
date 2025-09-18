import pyodbc

conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=.;DATABASE=EduManager;Trusted_Connection=yes;')
cursor = conn.cursor()

# Statistiques globales
cursor.execute('SELECT COUNT(*) FROM eleves')
total = cursor.fetchone()[0]
print(f'Total élèves: {total}')

cursor.execute("SELECT COUNT(*) FROM eleves WHERE genre = 'M'")
garcons = cursor.fetchone()[0]
print(f'Garçons: {garcons}')

cursor.execute("SELECT COUNT(*) FROM eleves WHERE genre = 'F'")
filles = cursor.fetchone()[0]
print(f'Filles: {filles}')

# Répartition par classe
cursor.execute("""
    SELECT c.nom_classe, c.niveau, COUNT(e.id_eleve) as nb_eleves
    FROM classes c
    LEFT JOIN eleves e ON c.id_classe = e.id_classe
    GROUP BY c.id_classe, c.nom_classe, c.niveau
    ORDER BY nb_eleves DESC
""")

print('\nRépartition par classe:')
for row in cursor.fetchall():
    print(f'  {row[0]} ({row[1]}): {row[2]} élèves')

conn.close()
