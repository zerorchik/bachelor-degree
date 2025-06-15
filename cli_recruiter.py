# from utils.io import (
#     load_all_candidates, load_all_vacancies, load_criteria_bank,
#     save_json, load_json, generate_next_id
# )
# from models.recruiter import Recruiter
# from models.vacancy import Vacancy
# from models.criteria import Criteria
# from models.scoring import Scoring
# import os
#
#
# def create_new_criterion():
#     print("\n📋 Додавання нового критерію")
#
#     cid = input("Назва критерію: ").strip()
#     question = input("Текст запитання: ").strip()
#
#     print("Оберіть тип критерію:")
#     type_options = ["scale", "category", "manual"]
#     for i, t in enumerate(type_options, 1):
#         print(f"{i}. {t}")
#     while True:
#         t_index = input("→ ").strip()
#         if t_index.isdigit() and 1 <= int(t_index) <= len(type_options):
#             ctype = type_options[int(t_index) - 1]
#             break
#         else:
#             print("❌ Невірний вибір. Введіть 1, 2 або 3.")
#
#     options = None
#
#     if ctype == "category":
#         print("Введіть варіанти відповіді та їх оцінки від 0 до 1. Enter — завершити:")
#         options = {}
#         while True:
#             label = input("Варіант відповіді: ").strip()
#             if not label:
#                 break
#             while True:
#                 score_input = input(f"Оцінка для '{label}': ").strip()
#                 try:
#                     score = float(score_input)
#                     if 0.0 <= score <= 1.0:
#                         options[label] = score
#                         break
#                     else:
#                         print("❌ Оцінка має бути від 0.0 до 1.0")
#                 except ValueError:
#                     print("❌ Введіть число (наприклад: 0.5)")
#
#     elif ctype == "scale":
#         print("Що краще: більша оцінка чи менша?")
#         print("1. Більша")
#         print("2. Менша")
#         while True:
#             direction = input("→ ").strip()
#             if direction == "1":
#                 options = {str(i): round(i * 0.2, 2) for i in range(1, 6)}
#                 break
#             elif direction == "2":
#                 options = {str(i): round(1.2 - i * 0.2, 2) for i in range(1, 6)}
#                 break
#             else:
#                 print("❌ Введіть 1 або 2")
#
#     # manual: options = None
#
#     crit = Criteria(cid, question, ctype, options)
#     path = os.path.join("data", "criteria_bank", f"{cid}.json")
#     save_json(crit.to_dict(), path)
#     print(f"✅ Критерій '{cid}' додано.")
#     return cid
#
#
# # def finalize_vacancy(vid, title, active_criteria):
# #     vacancy = Vacancy(vid, title, active_criteria)
# #     save_json(vacancy.to_dict(), os.path.join("data", "vacancies", f"{vid}.json"))
# #     print(f"✅ Вакансію {vid} збережено.")
#
# def finalize_vacancy(vid, title, active_criteria, recruiter_id):
#     vacancy = Vacancy(vid, title, active_criteria, recruiter_id)
#     save_json(vacancy.to_dict(), os.path.join("data", "vacancies", f"{vid}.json"))
#     print(f"✅ Вакансію {vid} збережено.")
#
#
# # def create_new_vacancy():
# #     vid = generate_next_id("data/vacancies", "V")
# #     print(f"\nID вакансії: {vid}")
# #     print(f"\n📝 Створення нової вакансії")
# #     title = input("Введіть назву вакансії: ").strip()
# #
# #     criteria_bank = load_criteria_bank("data/criteria_bank")
# #     active_criteria = {}
# #
# #     while True:
# #         while True:
# #             print("\nОберіть критерій, яким має володіти кандидат:")
# #             all_criteria = list(criteria_bank.items())  # (cid, Criteria)
# #             for i, (cid, crit_obj) in enumerate(all_criteria, 1):
# #                 print(f"{i}. {cid} ({crit_obj.type})")
# #             print("0. ➕ Додати новий критерій")
# #             print("q. ❌ Завершити створення вакансії")
# #
# #             choice = input("→ ").strip().lower()
# #             if choice == "0":
# #                 new_id = create_new_criterion()
# #                 criteria_bank = load_criteria_bank("data/criteria_bank")
# #                 continue
# #
# #             elif choice == "q":
# #                 if not active_criteria:
# #                     print("⚠ Створення вакансії скасовано, оскільки не вибрано жодного критерію.")
# #                     return
# #                 else:
# #                     return finalize_vacancy(vid, title, active_criteria)
# #
# #             elif choice.isdigit() and 1 <= int(choice) <= len(all_criteria):
# #                 selected_crit = all_criteria[int(choice) - 1]
# #                 cid = selected_crit[0]
# #                 crit = selected_crit[1]
# #
# #                 print(f"\n📌 Критерій: {cid}")
# #                 print(f"Тип: {crit.type}")
# #                 print(f"Питання: {crit.question}")
# #                 if crit.options:
# #                     print("Варіанти оцінювання:")
# #                     for k, v in crit.options.items():
# #                         print(f"- {k}: {v}")
# #
# #                 print("\nЩо зробити?")
# #                 print("1. Додати цей критерій до вакансії")
# #                 print("2. Повернутись до списку")
# #
# #                 while True:
# #                     act = input("→ ").strip()
# #                     if act == "1":
# #                         while True:
# #                             weight_input = input("Вага критерію (1–5): ").strip()
# #                             if weight_input.isdigit() and 1 <= int(weight_input) <= 5:
# #                                 weight = int(weight_input)
# #                                 break
# #                             else:
# #                                 print("❌ Неправильне значення. Введіть число від 1 до 5.")
# #                         active_criteria[cid] = {"active": 1, "weight": weight}
# #                         break
# #                     elif act == "2":
# #                         break
# #                     else:
# #                         print("❌ Введіть 1 або 2.")
# #                 if act == "1":
# #                     break  # завершити внутрішній цикл, перейти до "Додати ще?"
# #             else:
# #                 print("❌ Невірний вибір.")
# #                 continue
# #
# #         print("\nДодати ще критерій?")
# #         print("1. Так")
# #         print("2. Ні")
# #         while True:
# #             cont = input("→ ").strip()
# #             if cont == "1":
# #                 break
# #             elif cont == "2":
# #                 return finalize_vacancy(vid, title, active_criteria)
# #             else:
# #                 print("❌ Невірний вибір. Введіть 1 або 2.")
#
# def create_new_vacancy(recruiter):
#     vid = generate_next_id("data/vacancies", "V")
#     print(f"\nID вакансії: {vid}")
#     print(f"\n📝 Створення нової вакансії")
#     title = input("Введіть назву вакансії: ").strip()
#
#     criteria_bank = load_criteria_bank("data/criteria_bank")
#     active_criteria = {}
#
#     while True:
#         while True:
#             print("\nОберіть критерій, яким має володіти кандидат:")
#             all_criteria = list(criteria_bank.items())  # (cid, Criteria)
#             for i, (cid, crit_obj) in enumerate(all_criteria, 1):
#                 print(f"{i}. {cid} ({crit_obj.type})")
#             print("0. ➕ Додати новий критерій")
#             print("q. ❌ Завершити створення вакансії")
#
#             choice = input("→ ").strip().lower()
#             if choice == "0":
#                 new_id = create_new_criterion()
#                 criteria_bank = load_criteria_bank("data/criteria_bank")
#                 continue
#
#             elif choice == "q":
#                 if not active_criteria:
#                     print("⚠ Створення вакансії скасовано, оскільки не вибрано жодного критерію.")
#                     return
#                 else:
#                     return finalize_vacancy(vid, title, active_criteria, recruiter.id)
#
#             elif choice.isdigit() and 1 <= int(choice) <= len(all_criteria):
#                 selected_crit = all_criteria[int(choice) - 1]
#                 cid = selected_crit[0]
#                 crit = selected_crit[1]
#
#                 print(f"\n📌 Критерій: {cid}")
#                 print(f"Тип: {crit.type}")
#                 print(f"Питання: {crit.question}")
#                 if crit.options:
#                     print("Варіанти оцінювання:")
#                     for k, v in crit.options.items():
#                         print(f"- {k}: {v}")
#
#                 print("\nЩо зробити?")
#                 print("1. Додати цей критерій до вакансії")
#                 print("2. Повернутись до списку")
#
#                 while True:
#                     act = input("→ ").strip()
#                     if act == "1":
#                         while True:
#                             weight_input = input("Вага критерію (1–5): ").strip()
#                             if weight_input.isdigit() and 1 <= int(weight_input) <= 5:
#                                 weight = int(weight_input)
#                                 break
#                             else:
#                                 print("❌ Неправильне значення. Введіть число від 1 до 5.")
#                         active_criteria[cid] = {"active": 1, "weight": weight}
#                         break
#                     elif act == "2":
#                         break
#                     else:
#                         print("❌ Введіть 1 або 2.")
#                 if act == "1":
#                     break  # завершити внутрішній цикл, перейти до "Додати ще?"
#             else:
#                 print("❌ Невірний вибір.")
#                 continue
#
#         print("\nДодати ще критерій?")
#         print("1. Так")
#         print("2. Ні")
#         while True:
#             cont = input("→ ").strip()
#             if cont == "1":
#                 break
#             elif cont == "2":
#                 return finalize_vacancy(vid, title, active_criteria, recruiter.id)
#             else:
#                 print("❌ Невірний вибір. Введіть 1 або 2.")
#
#
# def evaluate_candidates(recruiter):
#     candidates = load_all_candidates("data/candidates")
#     vacancies = load_all_vacancies("data/vacancies")
#     relevant_criteria = set()
#
#     for v in vacancies:
#         if v.recruiter_id == recruiter.id:
#             relevant_criteria.update(v.get_criteria_ids())
#
#     updated = False
#     for c in candidates:
#         for r in c.responses.values():
#             if r.is_pending() and r.criterion_id in relevant_criteria:
#                 print(f"\nКандидат {c.id}, критерій {r.criterion_id}")
#                 print(f"Відповідь: {r.raw_answer}")
#                 while True:
#                     s_input = input("Оцінка (0.0–1.0): ").strip()
#                     try:
#                         s = float(s_input)
#                         if 0.0 <= s <= 1.0:
#                             r.assign_score(s)
#                             break
#                         else:
#                             print("❌ Оцінка має бути від 0.0 до 1.0")
#                     except ValueError:
#                         print("❌ Введіть число, наприклад: 0.75")
#                 updated = True
#     if updated:
#         for c in candidates:
#             save_json(c.to_dict(), os.path.join("data", "candidates", f"{c.id}.json"))
#         print("✅ Оцінки збережено.")
#     else:
#         print("✔ Немає відкритих відповідей.")
#
#
# # def run_recruiter_cli():
# #     print("\n🧑‍💼 Інтерфейс рекрутера")
# #     print("1. Додати критерій")
# #     print("2. Додати вакансію")
# #     print("3. Оцінити відповіді кандидатів")
# #     print("4. Згенерувати CSV відповідностей")
# #     print("0. Вийти")
# #     cmd = input("Оберіть дію: ").strip()
# #
# #     base = "data"
# #     if cmd == "1":
# #         create_new_criterion()
# #
# #     elif cmd == "2":
# #         create_new_vacancy()
# #
# #     elif cmd == "3":
# #         candidates = load_all_candidates(os.path.join(base, "candidates"))
# #         updated = False
# #         for c in candidates:
# #             for r in c.responses.values():
# #                 if r.is_pending():
# #                     print(f"\nКандидат {c.id}, критерій {r.criterion_id}")
# #                     print(f"Відповідь: {r.raw_answer}")
# #                     while True:
# #                         s_input = input("Оцінка (0.0–1.0): ").strip()
# #                         try:
# #                             s = float(s_input)
# #                             if 0.0 <= s <= 1.0:
# #                                 r.assign_score(s)
# #                                 break
# #                             else:
# #                                 print("❌ Оцінка має бути від 0.0 до 1.0")
# #                         except ValueError:
# #                             print("❌ Введіть число, наприклад: 0.75")
# #                     updated = True
# #         if updated:
# #             for c in candidates:
# #                 save_json(c.to_dict(), os.path.join(base, "candidates", f"{c.id}.json"))
# #             print("✅ Оцінки збережено.")
# #         else:
# #             print("✔ Немає відкритих відповідей.")
# #
# #     elif cmd == "4":
# #         cands = load_all_candidates(os.path.join(base, "candidates"))
# #         vacs = load_all_vacancies(os.path.join(base, "vacancies"))
# #         bank = load_criteria_bank(os.path.join(base, "criteria_bank"))
# #         scoring = Scoring()
# #         matrix = scoring.compute_matrix(cands, vacs, bank)
# #         scoring.export_to_csv(matrix, os.path.join(base, "results", "matrix.csv"))
# #
# #     elif cmd == "0":
# #         return
# #
# #     else:
# #         print("❌ Невідома команда.")
# #
# #     run_recruiter_cli()
#
#
# def run_recruiter_cli():
#     # print("\n🧑‍💼 Вхід до системи рекрутера")
#     # recruiter_id = input("Ваш ID: ").strip()
#     # recruiter_name = input("Ваше ім’я: ").strip()
#     # recruiter = Recruiter(recruiter_id, recruiter_name)
#
#     print("\n🔐 Вхід або реєстрація")
#     print("1. Увійти")
#     print("2. Зареєструватися")
#
#     choice = input("→ ").strip()
#     if choice == "2":
#         recruiter_id = generate_next_id("data/recruiters", "R")
#         name = input("Ваше ім’я: ").strip()
#         password = input("Придумайте пароль: ").strip()
#         recruiter = Recruiter(recruiter_id, name, password)
#         save_recruiter(recruiter, "data/recruiters")
#         print(f"✅ Рекрутер зареєстрований з ID {recruiter_id}")
#     elif choice == "1":
#         recruiter_id = input("Ваш ID: ").strip()
#         password = input("Пароль: ").strip()
#         path = os.path.join("data/recruiters", f"{recruiter_id}.json")
#         if not os.path.exists(path):
#             print("❌ Рекрутер не знайдений.")
#             return
#         data = load_json(path)
#         if data["password"] != password:
#             print("❌ Невірний пароль.")
#             return
#         recruiter = Recruiter.from_dict(data)
#
#     base = "data"
#
#     while True:
#         print("\n🧑‍💼 Інтерфейс рекрутера")
#         print("1. Додати критерій")
#         print("2. Додати вакансію")
#         print("3. Оцінити відповіді кандидатів")
#         print("4. Згенерувати CSV відповідностей")
#         print("5. Переглянути мої вакансії")
#         print("0. Вийти")
#         cmd = input("Оберіть дію: ").strip()
#
#         if cmd == "1":
#             create_new_criterion()
#
#         elif cmd == "2":
#             create_new_vacancy(recruiter)
#
#         elif cmd == "3":
#             evaluate_candidates(recruiter)
#
#         elif cmd == "4":
#             cands = load_all_candidates(os.path.join(base, "candidates"))
#             vacs = load_all_vacancies(os.path.join(base, "vacancies"))
#             bank = load_criteria_bank(os.path.join(base, "criteria_bank"))
#
#             # Фільтрація вакансій лише цього рекрутера
#             vacs = [v for v in vacs if v.recruiter_id == recruiter.id]
#             scoring = Scoring()
#             matrix = scoring.compute_matrix(cands, vacs, bank)
#             scoring.export_to_csv(matrix, os.path.join(base, "results", f"matrix_{recruiter.id}.csv"))
#
#         elif cmd == "5":
#             my_vacs = [v for v in load_all_vacancies("data/vacancies") if v.recruiter_id == recruiter.id]
#             if not my_vacs:
#                 print("ℹ У вас ще немає створених вакансій.")
#             for v in my_vacs:
#                 print(f"\n📌 {v.id}: {v.title}")
#                 for cid, cfg in v.active_criteria.items():
#                     print(f" - {cid}: вага {cfg['weight']}")
#
#         elif cmd == "0":
#             return
#
#         else:
#             print("❌ Невідома команда.")

import os
import hashlib
from utils.io import (
    load_all_candidates, load_all_vacancies, load_criteria_bank,
    save_json, load_json, generate_next_id
)
from models.recruiter import Recruiter
from models.vacancy import Vacancy
from models.criteria import Criteria
from models.scoring import Scoring


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def load_all_recruiters(path="data/recruiters"):
    recruiters = {}
    for fname in os.listdir(path):
        if fname.endswith(".json"):
            data = load_json(os.path.join(path, fname))
            recruiters[data["id"]] = data
    return recruiters


def login_or_register():
    recruiters = load_all_recruiters()
    while True:
        print("\n🧑‍💼 Вхід до системи")
        print("1. Увійти")
        print("2. Зареєструватися")
        print("0. Вийти")

        choice = input("→ ").strip()
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
            print("❌ Невірний вибір.")


def register_recruiter(recruiters):
    while True:
        name = input("\nВаше ім’я (або 0 для повернення): ").strip()
        if name == "0":
            return None
        if any(r["name"] == name for r in recruiters.values()):
            print("❌ Користувач з таким іменем уже існує.")
            continue
        password = input("Встановіть пароль: ").strip()
        rid = generate_next_id("data/recruiters", "R")
        hashed = hash_password(password)
        data = {"id": rid, "name": name, "password": hashed}
        save_json(data, os.path.join("data/recruiters", f"{rid}.json"))
        print(f"✅ Рекрутер зареєстрований з ID {rid}")
        return Recruiter(rid, name)


def authorize_recruiter(recruiters):
    while True:
        name = input("\nВаше ім’я (або 0 для повернення): ").strip()
        if name == "0":
            return None

        # Шукаємо рекрутера за ім’ям
        found = next((r for r in recruiters.values() if r["name"] == name), None)
        if not found:
            print("❌ Користувача з таким іменем не знайдено.")
            continue

        # Запитуємо пароль з можливістю повернення
        while True:
            password = input("Пароль (або 0 для повернення): ").strip()
            if password == "0":
                break  # назад до введення імені
            if found["password"] == hash_password(password):
                print(f"✅ Успішний вхід.\n\nВаш ID: {found['id']}")
                return Recruiter(found["id"], found["name"])
            else:
                print("❌ Невірний пароль.")


def create_new_criterion():
    print("\n📋 Додавання нового критерію")
    cid = input("Назва критерію: ").strip()
    question = input("Текст запитання: ").strip()

    print("Оберіть тип критерію:")
    type_options = ["scale", "category", "manual"]
    for i, t in enumerate(type_options, 1):
        print(f"{i}. {t}")
    while True:
        t_index = input("→ ").strip()
        if t_index.isdigit() and 1 <= int(t_index) <= len(type_options):
            ctype = type_options[int(t_index) - 1]
            break
        else:
            print("❌ Введіть 1, 2 або 3.")

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
                        print("❌ Введіть число від 0.0 до 1.0")
                except ValueError:
                    print("❌ Введіть число (наприклад 0.5)")

    elif ctype == "scale":
        print("Що краще: більша оцінка чи менша?")
        print("1. Більша")
        print("2. Менша")
        while True:
            direction = input("→ ").strip()
            if direction == "1":
                options = {str(i): round(i * 0.2, 2) for i in range(1, 6)}
                break
            elif direction == "2":
                options = {str(i): round(1.2 - i * 0.2, 2) for i in range(1, 6)}
                break
            else:
                print("❌ Введіть 1 або 2")

    crit = Criteria(cid, question, ctype, options)
    save_json(crit.to_dict(), os.path.join("data", "criteria_bank", f"{cid}.json"))
    print(f"✅ Критерій '{cid}' додано.")
    return cid


def finalize_vacancy(vid, title, active_criteria, recruiter_id):
    vacancy = Vacancy(vid, title, active_criteria, recruiter_id)
    save_json(vacancy.to_dict(), os.path.join("data", "vacancies", f"{vid}.json"))
    print(f"✅ Вакансію {vid} збережено.")


def create_new_vacancy(recruiter):
    vid = generate_next_id("data/vacancies", "V")
    print(f"\nID вакансії: {vid}")
    title = input("Введіть назву вакансії: ").strip()
    criteria_bank = load_criteria_bank("data/criteria_bank")
    active_criteria = {}

    while True:
        print("\nОберіть критерій:")
        all_criteria = list(criteria_bank.items())
        for i, (cid, crit) in enumerate(all_criteria, 1):
            print(f"{i}. {cid} ({crit.type})")
        print("0. ➕ Додати новий")
        print("q. ❌ Завершити")

        choice = input("→ ").strip().lower()
        if choice == "0":
            create_new_criterion()
            criteria_bank = load_criteria_bank("data/criteria_bank")
            continue
        elif choice == "q":
            if not active_criteria:
                print("⚠ Створення скасовано: жодного критерію не вибрано.")
                return
            return finalize_vacancy(vid, title, active_criteria, recruiter.id)
        elif choice.isdigit() and 1 <= int(choice) <= len(all_criteria):
            cid, crit = all_criteria[int(choice) - 1]
            print(f"\n📌 {cid} ({crit.type}) — {crit.question}")
            if crit.options:
                print("Варіанти:")
                for k, v in crit.options.items():
                    print(f"  - {k}: {v}")
            print("\n1. Додати до вакансії\n2. Назад")
            act = input("→ ").strip()
            if act == "1":
                while True:
                    w = input("Вага (1–5): ").strip()
                    if w.isdigit() and 1 <= int(w) <= 5:
                        active_criteria[cid] = {"active": 1, "weight": int(w)}
                        break
                    print("❌ Невірне значення.")
        else:
            print("❌ Невірний вибір.")


def evaluate_candidates(recruiter):
    candidates = load_all_candidates("data/candidates")
    vacancies = load_all_vacancies("data/vacancies")
    relevant_criteria = set()
    for v in vacancies:
        if v.recruiter_id == recruiter.id:
            relevant_criteria.update(v.get_criteria_ids())

    updated = False
    for c in candidates:
        for r in c.responses.values():
            if r.is_pending() and r.criterion_id in relevant_criteria:
                print(f"\nКандидат {c.id}, критерій {r.criterion_id}")
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
                            print("❌ Введіть значення від 0 до 1")
                    except:
                        print("❌ Некоректне число")
    if updated:
        for c in candidates:
            save_json(c.to_dict(), f"data/candidates/{c.id}.json")
        print("✅ Збережено.")
    else:
        print("\n✔ Оцінювати нічого.")


def view_recruiter_vacancies(recruiter):
    vacancies = load_all_vacancies("data/vacancies")
    print(f"\n📄 Вакансії рекрутера {recruiter.id}:")
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
        print("🚪 Вихід із системи.")
        return

    while True:
        print("\n🧑‍💼 Меню рекрутера")
        print("1. Додати критерій")
        print("2. Додати вакансію")
        print("3. Переглянути мої вакансії")
        print("4. Оцінити кандидатів")
        print("5. Згенерувати CSV")
        print("0. Вийти")

        cmd = input("→ ").strip()
        if cmd == "1":
            create_new_criterion()
        elif cmd == "2":
            create_new_vacancy(recruiter)
        elif cmd == "3":
            view_recruiter_vacancies(recruiter)
        elif cmd == "4":
            evaluate_candidates(recruiter)
        elif cmd == "5":
            scoring = Scoring()
            cands = load_all_candidates("data/candidates")
            vacs = load_all_vacancies("data/vacancies")
            bank = load_criteria_bank("data/criteria_bank")
            own_vacs = [v for v in vacs if v.recruiter_id == recruiter.id]
            matrix = scoring.compute_matrix(cands, own_vacs, bank)
            scoring.export_to_csv(matrix, f"data/results/matrix_{recruiter.id}.csv")
        elif cmd == "0":
            break
        else:
            print("❌ Невірна команда.")
