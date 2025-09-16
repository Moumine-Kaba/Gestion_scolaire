class Matiere:
    def __init__(self, id, nom, description=None, coefficient=None):
        self.id = id
        self.nom = nom
        self.description = description
        self.coefficient = coefficient

    def to_tuple(self):
        return (self.id, self.nom, self.description, self.coefficient)
