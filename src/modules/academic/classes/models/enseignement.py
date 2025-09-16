class Enseignement:
    def __init__(self, id, professeur_id, classe_id, matiere_id, salle_id=None):
        self.id = id
        self.professeur_id = professeur_id
        self.classe_id = classe_id
        self.matiere_id = matiere_id
        self.salle_id = salle_id

    def to_tuple(self):
        return (self.id, self.professeur_id, self.classe_id, self.matiere_id, self.salle_id)
