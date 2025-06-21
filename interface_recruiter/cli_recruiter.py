import os
import hashlib
from utils.io import (
    load_all_candidates, load_all_vacancies, load_criteria_bank,
    save_json, load_json, generate_next_id
)
from models.recruiter import Recruiter
from models.vacancy import Vacancy
from models.candidate_response import CandidateResponse
from models.criteria import Criteria
from models.scoring import Scoring


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def load_all_recruiters(path="../data/recruiters"):
    recruiters = {}
    for fname in os.listdir(path):
        if fname.endswith(".json"):
            data = load_json(os.path.join(path, fname))
            recruiters[data["id"]] = data
    return recruiters


def login_or_register():
    recruiters = load_all_recruiters()
    while True:
        print("\n------------------------------------")
        print("\tВхід до системи")
        print("------------------------------------")
        print("1. Увійти")
        print("2. Зареєструватися")
        print("0. Вийти")

        choice = input("-> ").strip()
        if choice == "1":
            recruiter = authorize_recruiter(recruiters)
            if recruiter:
                return recruiter
        elif choice == "2":
            recruiter = register_recruiter(recruiters)
            if recruiter:
                return recruiter
        elif choice == "0":
            return None
        else:
            print("X - Невірний вибір.")


def register_recruiter(recruiters):
    while True:
        name = input("\nВаше ім’я (або 0 для повернення): ").strip()
        if name == "0":
            return None
        if any(r["name"] == name for r in recruiters.values()):
            print("X - Користувач з таким іменем уже існує.")
            continue
        password = input("Встановіть пароль: ").strip()
        rid = generate_next_id("../data/recruiters", "R")
        hashed = hash_password(password)
        data = {"id": rid, "name": name, "password": hashed}
        save_json(data, os.path.join("../data/recruiters", f"{rid}.json"))
        print(f"OK - Рекрутер зареєстрований з ID {rid}")
        return Recruiter(rid, name)


def authorize_recruiter(recruiters):
    while True:
        name = input("\nВаше ім’я (або 0 для повернення): ").strip()
        if name == "0":
            return None

        # Шукаємо рекрутера за ім’ям
        found = next((r for r in recruiters.values() if r["name"] == name), None)
        if not found:
            print("X - Користувача з таким іменем не знайдено.")
            continue

        # Запитуємо пароль з можливістю повернення
        while True:
            password = input("Пароль (або 0 для повернення): ").strip()
            if password == "0":
                break  # назад до введення імені
            if found["password"] == hash_password(password):
                print(f"OK - Успішний вхід.\n\nВаш ID: {found['id']}")
                return Recruiter(found["id"], found["name"])
            else:
                print("X - Невірний пароль.")


def create_new_criterion():
    print("\n------------------------------------")
    print("\tДодавання нового критерію")
    print("------------------------------------")
    cid = input("Назва критерію: ").strip()
    question = input("Текст запитання: ").strip()

    print("Оберіть тип критерію:")
    type_options = ["scale", "category", "manual"]
    for i, t in enumerate(type_options, 1):
        print(f"{i}. {t}")
    while True:
        t_index = input("-> ").strip()
        if t_index.isdigit() and 1 <= int(t_index) <= len(type_options):
            ctype = type_options[int(t_index) - 1]
            break
        else:
            print("X - Введіть 1, 2 або 3.")

    options = None
    if ctype == "category":
        print("Введіть варіанти відповіді та їх оцінки від 0 до 1. Enter — завершити:")
        options = {}
        while True:
            label = input("Варіант відповіді: ").strip()
            if not label:
                break
            while True:
                score_input = input(f"Оцінка для '{label}': ").strip()
                try:
                    score = float(score_input)
                    if 0.0 <= score <= 1.0:
                        options[label] = score
                        break
                    else:
                        print("X - Введіть число від 0.0 до 1.0")
                except ValueError:
                    print("X - Введіть число (наприклад 0.5)")

    elif ctype == "scale":
        print("Що краще: більша оцінка чи менша?")
        print("1. Більша")
        print("2. Менша")
        while True:
            direction = input("-> ").strip()
            if direction == "1":
                options = {str(i): round(i * 0.2, 2) for i in range(1, 6)}
                break
            elif direction == "2":
                options = {str(i): round(1.2 - i * 0.2, 2) for i in range(1, 6)}
                break
            else:
                print("X - Введіть 1 або 2")

    crit = Criteria(cid, question, ctype, options)
    save_json(crit.to_dict(), os.path.join("../data", "criteria_bank", f"{cid}.json"))
    print(f"OK - Критерій '{cid}' додано.")
    return cid


def finalize_vacancy(vid, title, active_criteria, recruiter_id):
    vacancy = Vacancy(vid, title, active_criteria, recruiter_id)
    save_json(vacancy.to_dict(), os.path.join("../data", "vacancies", f"{vid}.json"))
    print(f"OK - Вакансію {vid} збережено.")


def create_new_vacancy(recruiter):
    vid = generate_next_id("../data/vacancies", "V")
    print(f"\nID вакансії: {vid}")
    title = input("Введіть назву вакансії: ").strip()
    criteria_bank = load_criteria_bank("../data/criteria_bank")
    active_criteria = {}

    while True:
        print("\nОберіть критерій:")
        all_criteria = list(criteria_bank.items())
        for i, (cid, crit) in enumerate(all_criteria, 1):
            print(f"{i}. {cid} ({crit.type})")
        print("0. (+) Додати новий")
        print("q. (X) Завершити")

        choice = input("-> ").strip().lower()
        if choice == "0":
            create_new_criterion()
            criteria_bank = load_criteria_bank("../data/criteria_bank")
            continue
        elif choice == "q":
            if not active_criteria:
                print("X - Створення скасовано: жодного критерію не вибрано.")
                return
            return finalize_vacancy(vid, title, active_criteria, recruiter.id)
        elif choice.isdigit() and 1 <= int(choice) <= len(all_criteria):
            cid, crit = all_criteria[int(choice) - 1]
            print(f"\n├── {cid} ({crit.type}) \n│   └── {crit.question}")
            if crit.options:
                print("Варіанти:")
                for k, v in crit.options.items():
                    print(f"  - {k}: {v}")
            print("\n1. Додати до вакансії\n2. Назад")
            act = input("-> ").strip()
            if act == "1":
                while True:
                    w = input("Вага (1–5): ").strip()
                    if w.isdigit() and 1 <= int(w) <= 5:
                        active_criteria[cid] = {"active": 1, "weight": int(w)}
                        break
                    print("X - Невірне значення.")
        else:
            print("X - Невірний вибір.")


def evaluate_candidates(recruiter):
    candidates = load_all_candidates("../data/candidates")
    vacancies = load_all_vacancies("../data/vacancies")
    criteria_bank = load_criteria_bank("../data/criteria_bank")

    # Вакансії, створені цим рекрутером
    recruiter_vacancies = {v.id: v for v in vacancies if v.recruiter_id == recruiter.id}
    relevant_criteria = {
        crit_id
        for v in recruiter_vacancies.values()
        for crit_id in v.get_criteria_ids()
    }

    updated = False

    for c in candidates:
        for vac_id, crit_dict in c.responses.items():
            if vac_id not in recruiter_vacancies:
                continue

            vacancy_title = recruiter_vacancies[vac_id].title

            for crit_id, r in crit_dict.items():
                # Якщо об'єкт ще не конвертований
                if isinstance(r, dict):
                    r = CandidateResponse(
                        criterion_id=crit_id,
                        response_type=r["type"],
                        raw_answer=r["raw_answer"],
                        score=r["score"],
                        status=r["status"]
                    )
                    c.responses[vac_id][crit_id] = r

                if r.is_pending() and crit_id in relevant_criteria:
                    question_text = criteria_bank[crit_id].question if crit_id in criteria_bank else "(питання не знайдено)"
                    print(f"\nКандидат {c.id}, вакансія {vacancy_title} ({vac_id}), критерій {crit_id}")
                    print(f"Питання: {question_text}")
                    print(f"Відповідь: {r.raw_answer}")
                    while True:
                        s = input("Оцінка (0.0–1.0): ").strip()
                        try:
                            val = float(s)
                            if 0 <= val <= 1:
                                r.assign_score(val)
                                updated = True
                                break
                            else:
                                print("X - Введіть значення від 0 до 1")
                        except ValueError:
                            print("X - Некоректне число")

    if updated:
        for c in candidates:
            save_json(c.to_dict(), f"data/candidates/{c.id}.json")
        print("OK - Збережено.")
    else:
        print("\nOK - Оцінювати нічого.")


def view_recruiter_vacancies(recruiter):
    vacancies = load_all_vacancies("../data/vacancies")
    print("\n------------------------------------")
    print(f"\tВакансії рекрутера {recruiter.id}:")
    print("------------------------------------")
    count = 0
    for v in vacancies:
        if v.recruiter_id == recruiter.id:
            print(f"- {v.id}: {v.title}")
            count += 1
    if count == 0:
        print(" (немає вакансій)")


def run_recruiter_cli():
    recruiter = login_or_register()
    if recruiter is None:
        print("\nX - Вихід із системи.")
        return

    while True:
        print("\n------------------------------------")
        print("\tМеню рекрутера")
        print("------------------------------------")
        print("1. Додати вакансію")
        print("2. Переглянути мої вакансії")
        print("3. Оцінити кандидатів")
        print("4. Згенерувати CSV")
        print("0. Вийти")

        cmd = input("-> ").strip()
        if cmd == "1":
            create_new_vacancy(recruiter)
        elif cmd == "2":
            view_recruiter_vacancies(recruiter)
        elif cmd == "3":
            evaluate_candidates(recruiter)
        elif cmd == "4":
            scoring = Scoring()
            cands = load_all_candidates("../data/candidates")
            vacs = load_all_vacancies("../data/vacancies")
            bank = load_criteria_bank("../data/criteria_bank")
            own_vacs = [v for v in vacs if v.recruiter_id == recruiter.id]
            matrix = scoring.compute_matrix(cands, own_vacs, bank)
            scoring.export_to_csv(matrix, f"../data/results/matrix_{recruiter.id}.csv")
        elif cmd == "0":
            break
        else:
            print("X - Невірна команда.")
