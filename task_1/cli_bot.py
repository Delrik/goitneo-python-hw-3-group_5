def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except KeyError as e:
            return str(e)
        except IndexError:
            return "Invalid number of arguments."

    return inner


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_contact(args, contacts):
    name, phone = args
    if name in contacts:
        raise KeyError("Contact already exists.")
    contacts[name] = phone
    return "Contact added."


@input_error
def change_contact(args, contacts):
    name, phone = args
    if name not in contacts:
        raise KeyError("Contact does not exist.")
    contacts[name] = phone
    return "Contact changed."


@input_error
def phone_contact(args, contacts):
    name = args[0]
    if name not in contacts:
        raise KeyError("Contact does not exist.")
    return f"{name}: {contacts[name]}"


@input_error
def all_contacts(args, contacts):
    return '\n'.join(f"{name}: {phone}" for name, phone in contacts.items())


def main():
    contacts = {}
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
        else:
            result = "Invalid command."
        print(result)
    print("Good bye!")


if __name__ == "__main__":
    main()
