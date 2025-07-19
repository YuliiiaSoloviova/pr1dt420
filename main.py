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
from collections import UserDict
from datetime import datetime, timedelta
import re


# === Моделі даних ===

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if not re.fullmatch(r"\d{10}", value):
            raise ValueError("Телефон має містити рівно 10 цифр.")
        super().__init__(value)


class Email(Field):
    def __init__(self, value):
        if value and not re.fullmatch(r"[^@]+@[^@]+\.[^@]+", value):
            raise ValueError("Невірний формат email.")
        super().__init__(value)


class Address(Field):
    pass


class Birthday(Field):
    def __init__(self, value):
        try:
            self.date = datetime.strptime(value, "%d.%m.%Y")
            super().__init__(value)
        except ValueError:
            raise ValueError("Неправильний формат. Використовуйте DD.MM.YYYY")


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.email = None
        self.address = None
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def add_email(self, email):
        self.email = Email(email)

    def add_address(self, address):
        self.address = Address(address)

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        phones = ', '.join(str(p) for p in self.phones) or "Немає"
        email = self.email.value if self.email else "Немає"
        address = self.address.value if self.address else "Немає"
        birthday = self.birthday.value if self.birthday else "Немає"
        return (f"Ім'я: {self.name.value}\n"
                f"Телефон(и): {phones}\n"
                f"Email: {email}\n"
                f"Адреса: {address}\n"
                f"День народження: {birthday}")


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self, days_ahead=7):
        today = datetime.today().date()
        result = []

        for record in self.data.values():
            if record.birthday:
                bday = record.birthday.date.date().replace(year=today.year)
                if bday < today:
                    bday = bday.replace(year=today.year + 1)
                delta = (bday - today).days
                if 0 <= delta <= days_ahead:
                    result.append((record.name.value, bday.strftime("%d.%m.%Y")))
        return result


# === Обробники ===

def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (IndexError, KeyError, ValueError) as e:
            return f"Помилка: {str(e)}"
    return wrapper


@input_error
def add_contact(book):
    name = input("Ім’я: ")
    phone = input("Телефон (10 цифр): ")
    email = input("Email: ")
    address = input("Адреса: ")
    birthday = input("День народження (DD.MM.YYYY): ")

    if name in book.data:
        return "Контакт з таким ім’ям вже існує."

    record = Record(name)
    if phone:
        record.add_phone(phone)
    if email:
        record.add_email(email)
    if address:
        record.add_address(address)
    if birthday:
        record.add_birthday(birthday)

    book.add_record(record)
    return "Контакт додано."


@input_error
def show_all_contacts(book):
    if not book.data:
        return "Контактів немає."
    return "\n\n".join(str(r) for r in book.data.values())


@input_error
def show_contact(book):
    name = input("Введіть ім’я контакту: ")
    record = book.find(name)
    if record:
        return str(record)
    return "Контакт не знайдено."


@input_error
def edit_contact(book):
    name = input("Введіть ім’я контакту, який потрібно редагувати: ")
    record = book.find(name)
    if not record:
        return "Контакт не знайдено."

    print(f"\nРедагуємо контакт: {record.name.value}")
    print("Залиште поле порожнім, якщо не хочете змінювати його.")

    new_name = input(f"Нове ім’я (зараз: {record.name.value}): ").strip()
    new_phone = input("Новий телефон (10 цифр): ").strip()
    new_email = input(f"Новий email (зараз: {record.email.value if record.email else 'немає'}): ").strip()
    new_address = input(f"Нова адреса (зараз: {record.address.value if record.address else 'немає'}): ").strip()
    new_birthday = input(f"Новий день народження (зараз: {record.birthday.value if record.birthday else 'немає'}): ").strip()

    if new_name:
        record.name = Name(new_name)
        book.data[new_name] = book.data.pop(name)

    if new_phone:
        record.phones = []
        record.add_phone(new_phone)

    if new_email:
        record.add_email(new_email)

    if new_address:
        record.add_address(new_address)

    if new_birthday:
        record.add_birthday(new_birthday)

    return "Контакт оновлено."


@input_error
def upcoming_birthdays(book):
    days_str = input("Через скільки днів показати дні народження? (наприклад: 7): ")
    days = int(days_str)

    upcoming = book.get_upcoming_birthdays(days)
    if not upcoming:
        return f"Немає днів народження протягом наступних {days} днів."
    return "\n".join([f"{name}: {date}" for name, date in upcoming])



# --- Нотатки Даша --- 
from datetime import datetime
import pickle


class Note:
    def __init__(self, text, tags=None):
        self.text = text
        self.created = datetime.now()
        self.tags = tags if tags else []

    def edit(self, new_text):
        self.text = new_text
        self.created = datetime.now()

    def __str__(self):
        tags_str = f" [теги: {', '.join(self.tags)}]" if self.tags else ""
        return f"{self.created.strftime('%Y-%m-%d %H:%M')} — {self.text}{tags_str}"


class NoteBook:
    def __init__(self):
        self.notes = []

    def add_note(self, text, tags=None):
        note = Note(text, tags)
        self.notes.append(note)
        return note

    def list_notes(self):
        if not self.notes:
            return "Нотаток немає."
        return "\n\n".join(f"{idx + 1}. {note}" for idx, note in enumerate(self.notes))

    def find_notes(self, keyword):
        result = [note for note in self.notes if keyword.lower() in note.text.lower()]
        return result

    def edit_note(self, index, new_text):
        if 0 <= index < len(self.notes):
            self.notes[index].edit(new_text)
            return True
        return False

    def delete_note(self, index):
        if 0 <= index < len(self.notes):
            del self.notes[index]
            return True
        return False

    def save_notes(self, filename="notebook.pkl"):
        with open(filename, "wb") as f:
            pickle.dump(self, f)

    @staticmethod
    def load_notes(filename="notebook.pkl"):
        try:
            with open(filename, "rb") as f:
                return pickle.load(f)
        except FileNotFoundError:
            return NoteBook()



from notes import NoteBook

notebook = NoteBook.load_notes()


def handle_add_note(args):
    if not args:
        return "Введіть текст нотатки після команди."
    text = args[0]
    tags = args[1:] if len(args) > 1 else []
    notebook.add_note(text, tags)
    return "Нотатку додано."


def handle_show_notes(_):
    return notebook.list_notes()


def handle_find_note(args):
    if not args:
        return "Введіть слово для пошуку."
    result = notebook.find_notes(args[0])
    if result:
        return "\n\n".join(str(note) for note in result)
    return "Нічого не знайдено."


def handle_edit_note(args):
    if len(args) < 2:
        return "Введіть номер нотатки та новий текст."
    try:
        index = int(args[0]) - 1
        new_text = " ".join(args[1:])
        if notebook.edit_note(index, new_text):
            return "Нотатку відредаговано."
        return "Нотатку не знайдено."
    except ValueError:
        return "Номер нотатки має бути числом."


def handle_delete_note(args):
    if len(args) < 1:
        return "Введіть номер нотатки для видалення."
    try:
        index = int(args[0]) - 1
        if notebook.delete_note(index):
            return "Нотатку видалено."
        return "Нотатку не знайдено."
    except ValueError:
        return "Номер нотатки має бути числом."


COMMANDS = {
    "add-note": handle_add_note,
    "show-notes": handle_show_notes,
    "find-note": handle_find_note,
    "edit-note": handle_edit_note,
    "delete-note": handle_delete_note,
}


def main():
    print("Персональний помічник з нотатками (введіть 'exit' для завершення)")
    while True:
        user_input = input(">> ").strip()
        if not user_input:
            continue
        if user_input.lower() in ("exit", "quit", "close"):
            notebook.save_notes()
            print("Нотатки збережено. До побачення!")
            break

        parts = user_input.split()
        command = parts[0].lower()
        args = parts[1:]

        handler = COMMANDS.get(command)
        if handler:
            result = handler(args)
            print(result)
        else:
            print("Невідома команда. Спробуйте ще раз.")


if __name__ == "__main__":
    main()




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

