class EmploiDuTemps:
    def __init__(self, id, jour, heure, matieres, professeurs, salles):
        self.id = id
        self.jour = jour
        self.heure = heure
        self.matieres = matieres
        self.professeurs = professeurs
        self.salles = salles

    def to_tuple(self):
        return (self.id, self.jour, self.heure, self.matieres, self.professeurs, self.salles)
