from collections import UserDict
from datetime import datetime, timedelta
import re
import pickle


# ==== Валідація полів (Марина) ====


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
        if value and not re.fullmatch(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", value):
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


# ==== Робота з контактами (Олена) ====


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


# ==== Нотатки (Даша) ====


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
        return "\n".join(f"{idx + 1}. {note}" for idx, note in enumerate(self.notes))

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


# ==== Збереження контактів (нове) ====

def save_contacts(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_contacts(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()


# ==== Меню та логіка взаємодії (Юля) ====

book = load_contacts()
notebook = NoteBook.load_notes()


def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (IndexError, KeyError, ValueError) as e:
            return f"Помилка: {str(e)}"
    return wrapper


@input_error
def add_contact():
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
def show_all_contacts():
    if not book.data:
        return "Контактів немає."
    return "\n\n".join(str(r) for r in book.data.values())


@input_error
def show_contact():
    name = input("Введіть ім’я контакту: ")
    record = book.find(name)
    return str(record) if record else "Контакт не знайдено."


@input_error
def edit_contact():
    name = input("Ім’я для редагування: ")
    record = book.find(name)
    if not record:
        return "Контакт не знайдено."
    new_phone = input("Новий телефон: ")
    record.phones = []
    record.add_phone(new_phone)
    return "Контакт оновлено."


@input_error
def delete_contact():
    name = input("Ім’я для видалення: ")
    book.delete(name)
    return "Контакт видалено."


@input_error
def list_birthdays():
    days = int(input("Кількість днів: "))
    upcoming = book.get_upcoming_birthdays(days)
    if not upcoming:
        return "Немає днів народження."
    return "\n".join([f"{name}: {date}" for name, date in upcoming])


@input_error
def add_note():
    text = input("Нотатка: ")
    tags = input("Теги (через кому): ").split(",")
    notebook.add_note(text, [t.strip() for t in tags])
    return "Нотатку додано."


@input_error
def search_notes():
    keyword = input("Ключове слово: ")
    found = notebook.find_notes(keyword)
    return "\n\n".join(str(n) for n in found) if found else "Нічого не знайдено."


@input_error
def edit_note():
    print(notebook.list_notes())
    idx = int(input("Номер нотатки: ")) - 1
    text = input("Новий текст: ")
    return "Оновлено." if notebook.edit_note(idx, text) else "Помилка."


@input_error
def delete_note():
    print(notebook.list_notes())
    idx = int(input("Номер для видалення: ")) - 1
    return "Видалено." if notebook.delete_note(idx) else "Помилка."


def main_menu():
    while True:
        print("\n" + "="*40)
        print("📘 Меню контактів та нотаток")
        print("="*40)
        print("1. Додати новий контакт")
        print("2. Показати всі контакти")
        print("3. Пошук у книзі контактів")
        print("4. Редагувати контакт")
        print("5. Видалити контакт")
        print("6. Список днів народження через N днів")
        print("7. Додати нотатку")
        print("8. Пошук у нотатках")
        print("9. Редагувати нотатку")
        print("10. Видалити нотатку")
        print("0. Вихід")
        choice = input("Оберіть дію: ")

        if choice == "1": print(add_contact())
        elif choice == "2": print(show_all_contacts())
        elif choice == "3": print(show_contact())
        elif choice == "4": print(edit_contact())
        elif choice == "5": print(delete_contact())
        elif choice == "6": print(list_birthdays())
        elif choice == "7": print(add_note())
        elif choice == "8": print(search_notes())
        elif choice == "9": print(edit_note())
        elif choice == "10": print(delete_note())
        elif choice == "0":
            notebook.save_notes()
            save_contacts(book)
            print("До побачення!")
            break
        else:
            print("Невірний вибір.")


if __name__ == "__main__":
    main_menu()