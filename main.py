from interface_candidate.cli_candidate import run_candidate_cli
from interface_recruiter.cli_recruiter import run_recruiter_cli

def main():
    print("\nСистема рекрутингу:")
    print("1. Кандидат")
    print("2. Рекрутер")
    role = input("Хто ви? ").strip()
    if role == "1":
        run_candidate_cli()
    elif role == "2":
        run_recruiter_cli()
    else:
        print("Невірний вибір")

if __name__ == "__main__":
    main()