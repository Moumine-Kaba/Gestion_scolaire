class Message:
    def __init__(self, id, expediteur_id, destinataire_id, contenu, date_envoi):
        self.id = id
        self.expediteur_id = expediteur_id
        self.destinataire_id = destinataire_id
        self.contenu = contenu
        self.date_envoi = date_envoi
