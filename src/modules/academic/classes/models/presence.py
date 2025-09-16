class Presence:
    def __init__(self, id, eleve_id, classe_id, professeur_id, date, statut, commentaire=None):
        self.id = id
        self.eleve_id = eleve_id
        self.classe_id = classe_id
        self.professeur_id = professeur_id
        self.date = date
        self.statut = statut
        self.commentaire = commentaire

    def to_tuple(self):
        return (self.id, self.eleve_id, self.classe_id, self.professeur_id, self.date, self.statut, self.commentaire)
