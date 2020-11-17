class Command:
    def __init__(self, name, params, response):
        self.name = name
        self.response = response
        self.parameters = params

    def matches(self, string):
        namelen = len(self.name)
        return string[:namelen] == self.name and len(string.split(self.name)[1]) >= len(self.parameters)


    def get_response(self, param="$"):
        return self.response.replace("$d", param)