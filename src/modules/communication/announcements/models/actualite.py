class Actualite:
    def __init__(self, id, titre, contenu, date):
        self.id = id
        self.titre = titre
        self.contenu = contenu
        self.date = date

    def to_tuple(self):
        return (self.id, self.titre, self.contenu, self.date)
