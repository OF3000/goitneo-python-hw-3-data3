from collections import UserDict
from typing import Optional
from datetime import datetime, timedelta


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Birthday(Field):
    pass


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if len(value) != 10:
            raise ValueError
        else:
            super().__init__(value)


class Record:
    def __init__(self, name, birthday: Optional[datetime] = None):
        self.name = Name(name)
        self.birthday = Birthday(birthday)
        self.phones = []

    def add_birthday(self, birthday):
        self.birthday = datetime.strptime(birthday, "%d.%m.%Y").date()

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones.pop(phone)

    def edit_phone(self, phone, nphone):
        for i, p in enumerate(self.phones):
            if p.value == phone:
                self.phones[i].value = nphone
                break

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p

    def show_birthday(self):
        return self.birthday

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday}"


class AddressBook(UserDict):
    def __init__(self):
        self.data = {}

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        for record in self.data:
            if record == name:
                return self.data.get(record)

    def delete(self, name):
        del self.data[name]


if __name__ == "__main__":
    print("-----------------------------------------")

    # # Створення нової адресної книги
    book = AddressBook()

    # # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    john_record.add_birthday("3.3.1995")
    print(john_record.show_birthday())

    # # Додавання запису John до адресної книги
    book.add_record(john_record)

    # # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record, name)

# # Знаходження та редагування телефону для John
# john = book.find("John")
# john.edit_phone("1234567890", "1112223333")

# print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

# # Пошук конкретного телефону у записі John
# found_phone = john.find_phone("5555555555")
# print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

# # Видалення запису Jane
# book.delete("Jane")
