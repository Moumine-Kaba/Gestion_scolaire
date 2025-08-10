class Salle:
    def __init__(self, id, nom, capacite=None, type=None):
        self.id = id
        self.nom = nom
        self.capacite = capacite
        self.type = type

    def to_tuple(self):
        return (self.id, self.nom, self.capacite, self.type)
