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


# === Меню ===

def print_menu():
    print("\n команду:")
    print("1. Додати новий контакт")
    print("2. Показати всі контакти")
    print("3. Редагувати контакт")
    print("4. Показати контакт за ім’ям")
    print("5. Показати дні народження через N днів")
    print("6. Вийти")


def main():
    book = AddressBook()
    print("👋 Ласкаво просимо до персонального помічника!")

    while True:
        print_menu()
        command = input("Введіть номер команди: ").strip()

        if command == "1":
            print(add_contact(book))
        elif command == "2":
            print(show_all_contacts(book))
        elif command == "3":
            print(edit_contact(book))
        elif command == "4":
            print(show_contact(book))
        elif command == "5":
            print(upcoming_birthdays(book))
        elif command == "6":
            print("До побачення! 👋")
            break
        else:
            print("Невідома команда. Спробуйте ще раз.")


if __name__ == "__main__":
    main()
