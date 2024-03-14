from datetime import date, timedelta
from bot_classes import AddressBook, Birthday, Record, Phone


def input_error(func):
    def inner(book, *args, **kwargs):
        try:
            return func(book, *args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
    return inner

@input_error
def add_contact(book, name, phone):
    record = Record(name)
    record.add_phone(phone.strip())
    book.add_record(record)
    return "Contact added."


@input_error
def change_contact(book, name, phone):
    record = book.find(name)
    if record:
        if record.phones:
            record.phones[0] = Phone(phone)
            return "Contact updated."
        else:
            return "No phone number found for this contact."
    else:
        return "Contact not found."

def show_phone(book, name):
    record = book.find(name)
    if record:
        return record.phones[0].value
    else:
        return "Contact not found."


@input_error
def add_birthday(book, name, birthday_str):
    record = book.find(name)
    if record:
        try:
            record.add_birthday(birthday_str)
            return "Birthday added."
        except ValueError as e:
            return str(e)
    else:
        return "Contact not found."

@input_error
def show_birthday(book, name):
    record = book.find(name)
    if record and record.birthday:
        return record.birthday.value
    else:
        return "Contact not found or birthday not set."

def show_all(book):
    return "\n".join([f"{record.name}: {record.phones[0].value}" for record in book.data.values()])

def birthdays_for_week(book):
    today = date.today()
    next_week = today + timedelta(days=7)
    birthdays = []
    for record in book.data.values():
        if record.birthday:
            birthday_month = record.birthday.date.month
            birthday_day = record.birthday.date.day
            this_years_birthday = date(today.year, birthday_month, birthday_day)
            if today <= this_years_birthday <= next_week:
                birthdays.append(f"{record.name}: {record.birthday.value}")
    return birthdays


def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ").strip()
        if user_input.lower() in ["close", "exit"]:
            print("Good bye!")
            break
        elif user_input.lower() == "hello":
            print("How can I help you?")
        elif user_input.lower().startswith("add "):
            _, name, phone = user_input.split(maxsplit=2)
            print(add_contact(book, name, phone))
        elif user_input.lower().startswith("change "):
            _, name, phone = user_input.split(maxsplit=2)
            print(change_contact(book, name, phone))
        elif user_input.lower().startswith("phone "):
            _, name = user_input.split(maxsplit=1)
            print(show_phone(book, name))
        elif user_input.lower().startswith("add-birthday "):
            _, name, birthday_str = user_input.split(maxsplit=2)
            print(add_birthday(book, name, birthday_str))
        elif user_input.lower().startswith("show-birthday "):
            _, name = user_input.split(maxsplit=1)
            print(show_birthday(book, name))
        elif user_input.lower() == "all":
            print(show_all(book))
        elif user_input.lower() == "birthdays":
            birthdays = birthdays_for_week(book)
            if birthdays:
                print("Upcoming birthdays:")
                for birthday in birthdays:
                    print(birthday)
            else:
                print("No birthdays this week.")
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
