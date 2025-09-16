class Paiement:
    def __init__(self, id, eleve_id, montant, date, mode_paiement=None, description=None):
        self.id = id
        self.eleve_id = eleve_id
        self.montant = montant
        self.date = date
        self.mode_paiement = mode_paiement
        self.description = description

    def to_tuple(self):
        return (self.id, self.eleve_id, self.montant, self.date, self.mode_paiement, self.description)
