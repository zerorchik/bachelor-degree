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

