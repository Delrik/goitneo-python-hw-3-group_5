import AddressBook


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return str(e)
        except KeyError as e:
            return str(e)
        except IndexError:
            return "Invalid number of arguments."
        except Exception as e:
            return f"Something went wrong: {str(e)}"

    return inner


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_contact(args, contacts: AddressBook.AddressBook):
    name, phone = args
    record = AddressBook.Record(name)
    record.add_phone(phone)
    contacts.add_record(record)
    return "Contact added."


@input_error
def change_contact(args, contacts: AddressBook.AddressBook):
    name, phone = args
    contacts.delete(name)
    record = AddressBook.Record(name)
    record.add_phone(phone)
    contacts.add_record(record)
    return "Contact changed."


@input_error
def phone_contact(args, contacts: AddressBook.AddressBook):
    name = args[0]
    record = contacts.find(name)
    return str(record)


@input_error
def all_contacts(args, contacts: AddressBook.AddressBook):
    return "\n".join(str(record) for record in contacts.data.values())


@input_error
def add_birthday(args, contacts: AddressBook.AddressBook):
    name, birthday = args
    record = contacts.find(name)
    record.add_birthday(birthday)
    return "Birthday added."


@input_error
def show_birthday(args, contacts: AddressBook.AddressBook):
    name = args[0]
    record = contacts.find(name)
    return record.birthday.value


@input_error
def birthdays(args, contacts: AddressBook.AddressBook):
    next_week_birthdays = contacts.get_birthdays_per_week()
    return "\n".join(f"{name}: {birthday}" for name, birthday in next_week_birthdays.items())


def main():
    contacts = AddressBook.AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        result = ""
        if command in ["close", "exit"]:
            break
        elif command == "hello":
            result = "How can I help you?"
        elif command == "add":
            result = add_contact(args, contacts)
        elif command == "change":
            result = change_contact(args, contacts)
        elif command == "phone":
            result = phone_contact(args, contacts)
        elif command == "all":
            result = all_contacts(args, contacts)
        elif command == "add-birthday":
            result = add_birthday(args, contacts)
        elif command == "show-birthday":
            result = show_birthday(args, contacts)
        elif command == "birthdays":
            result = birthdays(args, contacts)
        elif command == "help":
            result = "Commands: hello, add, change, phone, all, add-birthday, show-birthday, birthdays, help, close, exit"
        else:
            result = "Invalid command."
        print(result)
    print("Good bye!")


if __name__ == "__main__":
    main()
