# class Recruiter:
#     def __init__(self, recruiter_id, name):
#         self.id = recruiter_id
#         self.name = name
#
#     def to_dict(self):
#         return {"id": self.id, "name": self.name}
#
#     @staticmethod
#     def from_dict(data):
#         return Recruiter(data["id"], data["name"])

class Recruiter:
    def __init__(self, recruiter_id, name):
        self.id = recruiter_id
        self.name = name

    def to_dict(self):
        return {"id": self.id, "name": self.name, "password": self.password}

    @staticmethod
    def from_dict(data):
        return Recruiter(data["id"], data["name"], data["password"])
