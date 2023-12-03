def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def add_contact(args, contacts):
    if len(args) != 2:
        return "Invalid number of arguments."
    name, phone = args
    if name in contacts:
        return "Contact already exists."
    contacts[name] = phone
    return "Contact added."


def change_contact(args, contacts):
    if len(args) != 2:
        return "Invalid number of arguments."
    name, phone = args
    if name not in contacts:
        return "Contact does not exist."
    contacts[name] = phone
    return "Contact changed."


def phone_contact(args, contacts):
    if len(args) != 1:
        return "Invalid number of arguments."
    name = args[0]
    if name not in contacts:
        return "Contact does not exist."
    return f"{name}: {contacts[name]}"


def all_contacts(args, contacts):
    if len(args) != 0:
        return "Invalid number of arguments."
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
