class Candidate:
    def __init__(self, candidate_id, responses):
        self.id = candidate_id
        self.responses = responses

    def is_complete(self):
        return all(r.is_scored() for r in self.responses.values())

    def get_response(self, criterion_id):
        return self.responses.get(criterion_id)

    def get_score_vector(self):
        return {cid: r.score for cid, r in self.responses.items() if r.score is not None}

    def to_dict(self):
        return {
            "id": self.id,
            "responses": {k: v.to_dict() for k, v in self.responses.items()}
        }

    @staticmethod
    def from_dict(data, CandidateResponse):
        responses = {
            k: CandidateResponse(
                criterion_id=k,
                response_type=v["type"],
                raw_answer=v["raw_answer"],
                score=v["score"],
                status=v["status"]
            ) for k, v in data["responses"].items()
        }
        return Candidate(candidate_id=data["id"], responses=responses)