import csv
import pandas as pd

class Scoring:
    def compute_score(self, candidate, vacancy, criteria_bank):
        numerator = 0.0
        denominator = 0
        for crit_id in vacancy.get_criteria_ids():
            if vacancy.is_criterion_used(crit_id):
                weight = vacancy.get_weight(crit_id)
                response = candidate.get_response(crit_id)
                score = response.score if response and response.score is not None else 0.0
                numerator += weight * score
                denominator += weight
        return numerator / denominator if denominator > 0 else 0.0

    def compute_matrix(self, candidates, vacancies, criteria_bank):
        matrix = {}
        for candidate in candidates:
            for vacancy in vacancies:
                score = self.compute_score(candidate, vacancy, criteria_bank)
                matrix[(candidate.id, vacancy.id)] = round(score, 4)
        return matrix


    def export_to_csv(self, matrix, filename):
        candidates = sorted(set(cid for cid, _ in matrix.keys()))
        vacancies = sorted(set(vid for _, vid in matrix.keys()))

        # Побудова DataFrame для табличного виводу
        df = pd.DataFrame(index=candidates, columns=vacancies)
        for cid in candidates:
            for vid in vacancies:
                df.loc[cid, vid] = matrix.get((cid, vid), "")

        print("\n📊 Матриця відповідності (кандидат × вакансія):")
        print(df.to_string())

        # Збереження в CSV з заміною крапки на кому
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=';')  # європейський стиль
            writer.writerow([""] + vacancies)
            for cid in candidates:
                row = [cid]
                for vid in vacancies:
                    value = matrix.get((cid, vid), "")
                    if isinstance(value, float):
                        value = f"{value:.4f}".replace(".", ",")
                    row.append(value)
                writer.writerow(row)

        print(f"\n📄 CSV файл збережено у {filename}")
