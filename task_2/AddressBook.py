from collections import UserDict
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


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

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
