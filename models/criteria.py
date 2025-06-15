class Criteria:
    def __init__(self, criterion_id, question, criterion_type, options=None):
        self.id = criterion_id
        self.question = question
        self.type = criterion_type
        self.options = options

    def normalize_answer(self, raw_answer):
        if self.type in ["scale", "category"] and self.options:
            return self.options.get(str(raw_answer), 0.0)
        raise ValueError("Manual criteria require manual scoring.")

    def to_dict(self):
        return {
            "id": self.id,
            "question": self.question,
            "type": self.type,
            "options": self.options
        }

    @staticmethod
    def from_dict(data):
        return Criteria(
            criterion_id=data["id"],
            question=data["question"],
            criterion_type=data["type"],
            options=data.get("options")
        )