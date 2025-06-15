# class Candidate:
#     def __init__(self, candidate_id, responses):
#         self.id = candidate_id
#         self.responses = responses
#
#     def is_complete(self):
#         return all(r.is_scored() for r in self.responses.values())
#
#     def get_response(self, criterion_id):
#         return self.responses.get(criterion_id)
#
#     def get_score_vector(self):
#         return {cid: r.score for cid, r in self.responses.items() if r.score is not None}
#
#     def to_dict(self):
#         return {
#             "id": self.id,
#             "responses": {k: v.to_dict() for k, v in self.responses.items()}
#         }
#
#     @staticmethod
#     def from_dict(data, CandidateResponse):
#         responses = {
#             k: CandidateResponse(
#                 criterion_id=k,
#                 response_type=v["type"],
#                 raw_answer=v["raw_answer"],
#                 score=v["score"],
#                 status=v["status"]
#             ) for k, v in data["responses"].items()
#         }
#         return Candidate(candidate_id=data["id"], responses=responses)


# from models.candidate_response import CandidateResponse
#
# class Candidate:
#     def __init__(self, candidate_id, name, password_hash, responses=None):
#         self.id = candidate_id
#         self.name = name
#         self.password_hash = password_hash
#         self.responses = responses if responses else {}
#
#     def add_responses_for_vacancy(self, vacancy_id, response_dict):
#         self.responses[vacancy_id] = response_dict
#
#     def has_applied_for(self, vacancy_id):
#         return vacancy_id in self.responses
#
#     def to_dict(self):
#         return {
#             "id": self.id,
#             "name": self.name,
#             "password": self.password_hash,
#             "responses": {
#                 vid: {cid: r.to_dict() for cid, r in resp.items()}
#                 for vid, resp in self.responses.items()
#             }
#         }
#
#     @staticmethod
#     def from_dict(data):
#         all_responses = {}
#         for vac_id, responses in data.get("responses", {}).items():
#             all_responses[vac_id] = {
#                 cid: CandidateResponse(
#                     criterion_id=cid,
#                     response_type=rd["type"],
#                     raw_answer=rd["raw_answer"],
#                     score=rd["score"],
#                     status=rd["status"]
#                 ) for cid, rd in responses.items()
#             }
#         return Candidate(
#             candidate_id=data["id"],
#             name=data["name"],
#             password_hash=data["password"],
#             responses=all_responses
#         )


# import hashlib
# from models.candidate_response import CandidateResponse
#
# class Candidate:
#     def __init__(self, candidate_id, name, password):
#         self.id = candidate_id
#         self.name = name
#         self.password = password  # зберігається вже хешований пароль
#         self.responses = {}
#
#     def to_dict(self):
#         return {
#             "id": self.id,
#             "name": self.name,
#             "password": self.password,
#             "responses": {k: v.to_dict() for k, v in self.responses.items()}
#         }
#
#     @staticmethod
#     def from_dict(data, CandidateResponse):
#         cand = Candidate(data["id"], data["name"], data["password"])
#         cand.responses = {
#             k: CandidateResponse(
#                 criterion_id=k,
#                 response_type=v["type"],
#                 raw_answer=v["raw_answer"],
#                 score=v["score"],
#                 status=v["status"]
#             ) for k, v in data.get("responses", {}).items()
#         }
#         return cand

from models.candidate_response import CandidateResponse

class Candidate:
    def __init__(self, candidate_id, name, password, responses=None):
        self.id = candidate_id
        self.name = name
        self.password = password  # зберігається хеш
        self.responses = responses if responses else {}  # {vacancy_id: {criterion_id: CandidateResponse}}

    def add_responses_for_vacancy(self, vacancy_id, response_dict):
        self.responses[vacancy_id] = response_dict

    def has_applied_for(self, vacancy_id):
        return vacancy_id in self.responses

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "password": self.password,
            "responses": {
                vid: {cid: r.to_dict() for cid, r in resp.items()}
                for vid, resp in self.responses.items()
            }
        }

    def get_response(self, vacancy_id, criterion_id):
        return self.responses.get(vacancy_id, {}).get(criterion_id)

    @staticmethod
    def from_dict(data, CandidateResponse):
        all_responses = {}
        for vac_id, responses in data.get("responses", {}).items():
            all_responses[vac_id] = {
                cid: CandidateResponse(
                    criterion_id=cid,
                    response_type=rd["type"],
                    raw_answer=rd["raw_answer"],
                    score=rd["score"],
                    status=rd["status"]
                ) for cid, rd in responses.items()
            }
        return Candidate(
            candidate_id=data["id"],
            name=data["name"],
            password=data["password"],
            responses=all_responses
        )

