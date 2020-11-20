class Command:
    def __init__(self, name, params, response, category):
        self.name = name
        self.response = response
        self.parameters = params
        self.category = category

    def matches(self, string):
        namelen = len(self.name)
        return string[:namelen] == self.name and len(
            list(filter(None, string.split(self.name)[1].strip().split("$")))) >= len(self.parameters)

    def get_response(self, params):
        response = self.response
        for index, param in enumerate(self.parameters):
            response = response.replace("$" + param, params[index])
        return response
