import re
from datetime import datetime, timedelta


# --- Дані ---
contacts = [
    {
        "ФІО": "Іваненко Іван Іванович",
        "Адреса": "Київ, вул. Хрещатик 1",
        "Телефон": "+380991112233",
        "Email": "ivan@gmail.com",
        "День народження": "2000-08-15"
    },
    {
        "ФІО": "Петренко Олена Миколаївна",
        "Адреса": "Львів, вул. Шевченка 22",
        "Телефон": "+380671234567",
        "Email": "olena@gmail.com",
        "День народження": "1995-07-20"
    }
]


notes = [
    {
        "Текст": "Купити подарунок",
        "ФІО": "Іваненко Іван Іванович"
    },
    {
        "Текст": "Подзвонити щодо зустрічі",
        "ФІО": "Петренко Олена Миколаївна"
    }
]


# --- Валідації Марина---



# --- Контакти Олена---



# --- Нотатки Даша --- 




# --- Меню Юля ---
def main_menu():
    while True:
        print("\n" + "="*40)
        print("📘 Меню контактів та нотаток")
        print("="*40)
        print("1. Додати новий контакт")
        print("2. Пошук у книзі контактів")
        print("3. Редагувати контакт")
        print("4. Видалити контакт")
        print("5. Список днів народження через N днів")
        print("6. Додати нотатку")
        print("7. Пошук у нотатках")
        print("8. Редагувати нотатку")
        print("9. Видалити нотатку")
        print("0. Вихід")
        choice = input("Оберіть дію: ")


        if choice == "1":
            add_contact()
        elif choice == "2":
            search_contacts()
        elif choice == "3":
            edit_contact()
        elif choice == "4":
            delete_contact()
        elif choice == "5":
            try:
                n = int(input("Введіть кількість днів: "))
                list_birthdays(n)
            except:
                print("❌ Введіть число.")
        elif choice == "6":
            add_note()
        elif choice == "7":
            search_notes()
        elif choice == "8":
            edit_note()
        elif choice == "9":
            delete_note()
        elif choice == "0":
            print("👋 Вихід з програми.")
            break
        else:
            print("❌ Невірний вибір.")
       
        pause()


# Запуск програми
if __name__ == "__main__":
    main_menu()

