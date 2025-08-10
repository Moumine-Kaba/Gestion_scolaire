class Utilisateur:
    def __init__(self, id, username, prenom, nom, email, telephone, password, role, niveau=None):
        self.id = id
        self.username = username
        self.prenom = prenom
        self.nom = nom
        self.email = email
        self.telephone = telephone
        self.password = password
        self.role = role
        self.niveau = niveau

    def to_tuple(self):
        return (self.id, self.username, self.prenom, self.nom, self.email, self.telephone, self.password, self.role, self.niveau)
