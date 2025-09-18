class Note:
    def __init__(self, id, eleve_id, matiere_id, notes, date=None):
        self.id = id
        self.eleve_id = eleve_id
        self.matiere_id = matiere_id
        self.notes = notes
        self.date = date

    def to_tuple(self):
        return (self.id, self.eleve_id, self.matiere_id, self.notes, self.date)
