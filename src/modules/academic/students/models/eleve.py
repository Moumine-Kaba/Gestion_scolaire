class Eleve:
    def __init__(self, id, nom, prenom, sexe, date_naissance, adresse, telephone_parent, email_parent, classe_id, photo_path=None, date_inscription=None, statut='actif'):
        self.id = id
        self.nom = nom
        self.prenom = prenom
        self.sexe = sexe
        self.date_naissance = date_naissance
        self.adresse = adresse
        self.telephone_parent = telephone_parent
        self.email_parent = email_parent
        self.classe_id = classe_id  # FK vers Classe
        self.photo_path = photo_path
        self.date_inscription = date_inscription
        self.statut = statut

    def to_tuple(self):
        return (self.id, self.nom, self.prenom, self.sexe, self.date_naissance, self.adresse, self.telephone_parent, self.email_parent, self.classe_id, self.photo_path, self.date_inscription, self.statut)
