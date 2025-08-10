class Professeur:
    def __init__(self, id, nom, prenom, sexe, telephone, email, specialite=None):
        self.id = id
        self.nom = nom
        self.prenom = prenom
        self.sexe = sexe
        self.telephone = telephone
        self.email = email
        self.specialite = specialite

    def to_tuple(self):
        return (self.id, self.nom, self.prenom, self.sexe, self.telephone, self.email, self.specialite)
