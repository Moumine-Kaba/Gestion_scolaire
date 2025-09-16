class Annonce:
    def __init__(self, id, titre, contenu, date, auteur_id=None):
        self.id = id
        self.titre = titre
        self.contenu = contenu
        self.date = date
        self.auteur_id = auteur_id  # FK utilisateur optionnel

    def to_tuple(self):
        return (self.id, self.titre, self.contenu, self.date, self.auteur_id)
