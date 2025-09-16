class Notification:
    def __init__(self, id, contenu, date, utilisateur_id=None, lu=False):
        self.id = id
        self.contenu = contenu
        self.date = date
        self.utilisateur_id = utilisateur_id  # FK utilisateur optionnel
        self.lu = lu  # Booléen pour savoir si la notif a été lue

    def to_tuple(self):
        return (self.id, self.contenu, self.date, self.utilisateur_id, int(self.lu))
