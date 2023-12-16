import datetime
from collections import UserDict
from collections import defaultdict
from functools import singledispatchmethod


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

    def __eq__(self, other):
        return self.value == other.value


class Name(Field):
    def __init__(self, value):
        super().__init__(value)


class Phone(Field):
    def __init__(self, value):
        if len(value) != 10 or not value.isnumeric():
            raise ValueError("Invalid phone number.")
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value):
        if value is not None:
            try:
                datetime.datetime.strptime(value, "%d.%m.%Y")
            except ValueError:
                raise ValueError("Invalid date.")
        super().__init__(value)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.birthday = Birthday(None)
        self.phones = []

    def add_birthday(self, birthday):
        if self.birthday.value is not None:
            raise ValueError("Birthday already exists.")
        if birthday is None:
            raise ValueError("Birthday can't be None.")
        self.birthday = Birthday(birthday)

    @singledispatchmethod
    def add_phone(self, phone):
        self.add_phone(Phone(phone))

    @add_phone.register
    def _(self, phone: Phone):
        self.phones.append(phone)

    @singledispatchmethod
    def remove_phone(self, phone):
        self.phones.remove(Phone(phone))

    @remove_phone.register
    def _(self, phone: Phone):
        self.phones.remove(phone)

    def edit_phone(self, old_phone, new_phone):
        if old_phone == new_phone:
            return
        old_phone_c = Phone(old_phone)
        new_phone_c = Phone(new_phone)
        self.remove_phone(old_phone_c)
        self.add_phone(new_phone_c)

    def find_phone(self, phone):
        return Phone(phone) in self.phones

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    def __init__(self):
        super().__init__()

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data[name]

    def delete(self, name):
        self.data.pop(name)

    def get_birthdays_per_week(self):
        result = defaultdict(list)
        current_date = datetime.datetime.now()
        for user in self.data.values():
            if not user.birthday.value:
                continue
            else:
                user_birthday = datetime.datetime.strptime(
                    user.birthday.value, "%d.%m.%Y").date()
                user_birthday = user_birthday.replace(year=current_date.year)
                if user_birthday < current_date.date():
                    user_birthday = user_birthday.replace(
                        year=current_date.year + 1)
                if (user_birthday - current_date.date()).days < 7:
                    date_name = user_birthday.strftime("%A")
                    if date_name in ["Saturday", "Sunday"] and current_date.strftime("%A") in ["Saturday", "Sunday", "Monday"]:
                        continue
                    if date_name in ["Saturday", "Sunday"]:
                        date_name = "Monday"
                    result[date_name].append(user.name.value)
        return result
