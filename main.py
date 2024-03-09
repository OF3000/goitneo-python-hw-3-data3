from adr_book import AddressBook, Record
from birthday import get_birthdays_per_week
from datetime import datetime, time


import pickle


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone(10 digits) please."
        except KeyError:
            return "No found."
        except IndexError:
            return "Index error"

    return inner


def sanitize_phone_number(phone):
    new_phone = (
        phone.strip()
        .removeprefix("+")
        .replace("(", "")
        .replace(")", "")
        .replace("-", "")
        .replace(" ", "")
    )
    return new_phone


@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_contact(args, contacts):
    name, phone = args
    record = Record(name)
    record.add_phone(sanitize_phone_number(phone))
    contacts.add_record(record)
    return "Contact added."


@input_error
def upd_contact(args, contacts):
    name, phone = args
    record = contacts.find(name)
    record.edit_phone(record.phones[0].value, sanitize_phone_number(phone))
    return "Contact changed."


@input_error
def get_contact(args, contacts):
    name = "".join(args)
    record = contacts.find(name)
    if not record:
        raise KeyError
    phone = record.phones[0].value
    return f"Phone is: {phone}"


def all_contact(contacts):
    res = ""
    for name, record in contacts.items():
        res += str(record) + "\n"
    return res


def save_data(file, contacts):
    with open(file, "wb") as f:
        pickle.dump(contacts, f)


def get_birthdays(contacts):
    users = []
    user = {}
    for name, record in contacts.items():
        if str(record.birthday) != "None":
            d = datetime.strptime(str(record.birthday), "%Y-%m-%d")
            user["name"] = name
            user["birthday"] = d
            users.append(user.copy())
    get_birthdays_per_week(users)


@input_error
def main():
    contacts = AddressBook()
    file_name = "book.bin"

    with open(file_name, "rb") as f:
        contacts = pickle.load(f)

    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, contacts))
            save_data(file_name, contacts)
        elif command == "change":
            print(upd_contact(args, contacts))
            save_data(file_name, contacts)
        elif command == "phone":
            print(get_contact(args, contacts))
        elif command == "all":
            print(all_contact(contacts))
        elif command == "add-birthday":
            if not contacts.find(args[0]):
                raise KeyError
            try:
                datetime.strptime(args[1], "%d.%m.%Y")
            except ValueError:
                print("Incorrect data format, should be DD.MM.YYYY")
                continue
            contacts.find(args[0]).add_birthday(args[1])
            print("Bitrhtay has been added")
        elif command == "show-birthday":
            print(f"{args[0]}'s is: {contacts.find(args[0]).show_birthday()}")
        elif command == "birthdays":
            get_birthdays(contacts)
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
