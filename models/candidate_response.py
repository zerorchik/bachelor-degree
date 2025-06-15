class CandidateResponse:
    def __init__(self, criterion_id, response_type, raw_answer, score, status):
        self.criterion_id = criterion_id
        self.type = response_type
        self.raw_answer = raw_answer
        self.score = score
        self.status = status

    def is_scored(self):
        return self.status == "scored"

    def is_pending(self):
        return self.status == "pending"

    def assign_score(self, score):
        self.score = score
        self.status = "scored"

    def to_dict(self):
        return {
            "type": self.type,
            "raw_answer": self.raw_answer,
            "score": self.score,
            "status": self.status
        }