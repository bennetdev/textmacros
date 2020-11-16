class Command:
    def __init__(self, name, response):
        self.name = name
        self.response = response

    def get_response(self):
        return self.response
