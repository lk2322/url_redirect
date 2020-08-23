class LinkAlreadyExistsError(Exception):
    def __init__(self, r_url, text='This link already exists in the database:'):
        self.text = text
        self.r_url = r_url

    def __str__(self):
        return self.text + self.url