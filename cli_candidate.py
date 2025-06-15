from utils.io import load_all_vacancies, load_criteria_bank, save_json, generate_next_id
from models.candidate_response import CandidateResponse
from models.candidate import Candidate
import os

def run_candidate_cli():
    base_path = "data"

    # Автоматична генерація ID кандидата
    cid = generate_next_id(os.path.join(base_path, "candidates"), "C")
    print(f"\nВаш ID: {cid}")
    responses = {}

    print("\n👤 Анкетування кандидата")

    # Завантаження вакансій і критеріїв
    vacancies = load_all_vacancies(os.path.join(base_path, "vacancies"))
    criteria_bank = load_criteria_bank(os.path.join(base_path, "criteria_bank"))

    # Вибір вакансії за номером
    print("Доступні вакансії:")
    for i, v in enumerate(vacancies, 1):
        print(f"{i}. {v.title} ({v.id})")
    while True:
        selected = input("Оберіть номер вакансії: ").strip()
        if selected.isdigit() and 1 <= int(selected) <= len(vacancies):
            vacancy = vacancies[int(selected) - 1]
            break
        else:
            print("❌ Невірний вибір. Спробуйте ще раз.")

    # Виведення опису вакансії
    print(f"\nВи обрали вакансію \"{vacancy.title}\", вона має {len(vacancy.get_criteria_ids())} критеріїв.")
    criteria_ids = vacancy.get_criteria_ids()

    # Проходження анкети
    for idx, crit_id in enumerate(criteria_ids, 1):
        if not vacancy.is_criterion_used(crit_id):
            continue

        crit = criteria_bank[crit_id]
        print(f"\nКритерій {idx} з {len(criteria_ids)}: {crit_id}")
        print(f"Питання: {crit.question} (тип: {crit.type})")

        if crit.type == "category" and crit.options:
            options_list = list(crit.options.keys())
            print("Можливі варіанти:")
            for opt_idx, opt in enumerate(options_list, 1):
                print(f"{opt_idx}. {opt}")
            while True:
                selected = input("Введіть номер варіанта: ").strip()
                if selected.isdigit() and 1 <= int(selected) <= len(options_list):
                    raw = options_list[int(selected) - 1]
                    break
                else:
                    print("❌ Невірний вибір. Спробуйте ще раз.")

        elif crit.type == "scale" and crit.options:
            print("Введіть значення від 1 до 5:")
            while True:
                raw = input("→ ").strip()
                if raw.isdigit() and raw in crit.options:
                    break
                else:
                    print("❌ Невірне значення. Введіть число від 1 до 5.")

        else:
            raw = input("→ ")

        # Збереження відповіді
        if crit.type in ["scale", "category"]:
            score = crit.normalize_answer(raw)
            responses[crit_id] = CandidateResponse(crit_id, crit.type, raw, score, "scored")
        else:
            responses[crit_id] = CandidateResponse(crit_id, crit.type, raw, None, "pending")

    # Збереження результатів
    candidate = Candidate(cid, responses)
    out_path = os.path.join(base_path, "candidates", f"{cid}.json")
    save_json(candidate.to_dict(), out_path)
    print(f"\n✅ Анкета кандидата {cid} збережена у {out_path}")
