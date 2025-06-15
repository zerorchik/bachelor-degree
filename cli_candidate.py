import os
import hashlib
from utils.io import (
    load_all_vacancies, load_criteria_bank, save_json, load_json,
    generate_next_id
)
from models.candidate import Candidate
from models.candidate_response import CandidateResponse


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def load_all_candidates(path="data/candidates"):
    candidates = {}
    for fname in os.listdir(path):
        if fname.endswith(".json"):
            data = load_json(os.path.join(path, fname))
            cand = Candidate.from_dict(data, CandidateResponse)
            candidates[cand.name] = cand
    return candidates


def login_or_register_candidate():
    candidates = load_all_candidates()
    while True:
        print("\n👤 Вхід до системи кандидата")
        print("1. Увійти")
        print("2. Зареєструватися")
        print("0. Вийти")

        choice = input("→ ").strip()
        if choice == "1":
            candidate = authorize_candidate(candidates)
            if candidate:
                return candidate
        elif choice == "2":
            candidate = register_candidate(candidates)
            if candidate:
                return candidate
        elif choice == "0":
            return None
        else:
            print("❌ Невірний вибір.")


def authorize_candidate(candidates):
    while True:
        name = input("\nВаше ім’я (або 0 для повернення): ").strip()
        if name == "0":
            return None
        if name not in candidates:
            print("❌ Кандидата не знайдено.")
            continue

        candidate = candidates[name]
        while True:
            password = input("Пароль (або 0 для повернення): ").strip()
            if password == "0":
                break  # Назад до імені
            if candidate.password == hash_password(password):
                print(f"✅ Вхід успішний.\n\nВаш ID: {candidate.id}")
                return candidate
            else:
                print("❌ Невірний пароль.")


def register_candidate(candidates):
    while True:
        name = input("\nВведіть ваше ім’я (або 0 для повернення): ").strip()
        if name == "0":
            return None
        if name in candidates:
            print("❌ Такий кандидат вже існує.")
            continue
        password = input("Встановіть пароль: ").strip()
        cid = generate_next_id("data/candidates", "C")
        hashed = hash_password(password)
        new_cand = Candidate(cid, name, hashed)
        save_json(new_cand.to_dict(), f"data/candidates/{cid}.json")
        print(f"✅ Успішна реєстрація. Ваш ID: {cid}")
        return new_cand


def run_candidate_cli():
    candidate = login_or_register_candidate()
    if candidate is None:
        return

    base_path = "data"
    vacancies = load_all_vacancies(os.path.join(base_path, "vacancies"))
    criteria_bank = load_criteria_bank(os.path.join(base_path, "criteria_bank"))

    while True:
        print("\n📋 Меню кандидата")
        print("1. Вакансії, на які ви подались")
        print("2. Інші доступні вакансії")
        print("0. Вийти")

        choice = input("→ ").strip()
        if choice == "0":
            break

        elif choice == "1":
            submitted_ids = candidate.responses.keys()
            submitted_vacancies = [v for v in vacancies if v.id in submitted_ids]
            if not submitted_vacancies:
                print("ℹ️ Ви ще не подались на жодну вакансію.")
                continue
            print("\n📄 Ви подались на:")
            for i, v in enumerate(submitted_vacancies, 1):
                print(f"{i}. {v.title} ({v.id})")

        elif choice == "2":
            submitted_ids = candidate.responses.keys()
            available_vacancies = [v for v in vacancies if v.id not in submitted_ids]
            if not available_vacancies:
                print("✔ Ви вже подались на всі доступні вакансії.")
                continue

            print("\n📄 Доступні вакансії:")
            for i, v in enumerate(available_vacancies, 1):
                print(f"{i}. {v.title} ({v.id})")
            print("0. Назад")

            index = input("Оберіть номер вакансії: ").strip()
            if index == "0":
                continue
            if not index.isdigit() or not (1 <= int(index) <= len(available_vacancies)):
                print("❌ Невірний вибір.")
                continue

            vacancy = available_vacancies[int(index) - 1]
            print(f"\n📌 Вакансія: {vacancy.title}")
            new_responses = {}

            for idx, crit_id in enumerate(vacancy.get_criteria_ids(), 1):
                if not vacancy.is_criterion_used(crit_id):
                    continue
                crit = criteria_bank[crit_id]
                print(f"\nКритерій {idx}/{len(vacancy.get_criteria_ids())}: {crit_id}")
                print(f"Питання: {crit.question} (тип: {crit.type})")

                if crit.type == "category" and crit.options:
                    options = list(crit.options.keys())
                    for i, opt in enumerate(options, 1):
                        print(f"{i}. {opt}")
                    while True:
                        sel = input("Оберіть варіант: ").strip()
                        if sel.isdigit() and 1 <= int(sel) <= len(options):
                            raw = options[int(sel) - 1]
                            break
                        print("❌ Невірний вибір.")

                elif crit.type == "scale" and crit.options:
                    print("Введіть значення від 1 до 5:")
                    while True:
                        raw = input("→ ").strip()
                        if raw in crit.options:
                            break
                        print("❌ Невірне значення.")

                else:
                    raw = input("→ ")

                if crit.type in ["scale", "category"]:
                    score = crit.normalize_answer(raw)
                    new_responses[crit_id] = CandidateResponse(crit_id, crit.type, raw, score, "scored")
                else:
                    new_responses[crit_id] = CandidateResponse(crit_id, crit.type, raw, None, "pending")

            candidate.add_responses_for_vacancy(vacancy.id, new_responses)
            save_json(candidate.to_dict(), f"data/candidates/{candidate.id}.json")
            print(f"✅ Анкета на \"{vacancy.title}\" збережена.")

        else:
            print("❌ Невірний вибір.")
