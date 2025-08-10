class EmploiDuTemps:
    def __init__(self, id, jour, heure, matiere, professeur, salle):
        self.id = id
        self.jour = jour
        self.heure = heure
        self.matiere = matiere
        self.professeur = professeur
        self.salle = salle

    def to_tuple(self):
        return (self.id, self.jour, self.heure, self.matiere, self.professeur, self.salle)
