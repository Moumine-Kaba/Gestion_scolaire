class Note:
    def __init__(self, id, eleve_id, matiere_id, note, date=None):
        self.id = id
        self.eleve_id = eleve_id
        self.matiere_id = matiere_id
        self.note = note
        self.date = date

    def to_tuple(self):
        return (self.id, self.eleve_id, self.matiere_id, self.note, self.date)
