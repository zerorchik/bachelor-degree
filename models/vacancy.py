class Vacancy:
    def __init__(self, vacancy_id, title, active_criteria, recruiter_id):
        self.id = vacancy_id
        self.title = title
        self.active_criteria = active_criteria
        self.recruiter_id = recruiter_id  # нове поле

    def get_criteria_ids(self):
        return list(self.active_criteria.keys())

    def get_weight(self, criterion_id):
        return self.active_criteria[criterion_id]["weight"]

    def is_criterion_used(self, criterion_id):
        return self.active_criteria.get(criterion_id, {}).get("active", 0) == 1

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "criteria": self.active_criteria,
            "recruiter_id": self.recruiter_id  # збереження нового поля
        }

    @staticmethod
    def from_dict(data):
        return Vacancy(
            vacancy_id=data["id"],
            title=data["title"],
            active_criteria=data["criteria"],
            recruiter_id=data.get("recruiter_id", "UNKNOWN")  # для сумісності зі старими вакансіями
        )
