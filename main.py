from ast import arg
from collections import UserDict
from datetime import datetime
from datetime import date
import shelve
import re


class Field:
    def __init__(self, value: str) -> None:
        self.value = value


class Name(Field):
    def __init__(self, value) -> None:
        super().__init__(value)
        self.__value = None
        self.value = value

    @property
    def name(self):
        return self.value

    @name.setter
    def name(self, value):
        self.__value = value


class Phone(Field):
    def __init__(self, value) -> None:
        super().__init__(value)
        self.__value = None
        self.value = value

    @property
    def phone(self):
        return self.__value

    @phone.setter
    def phone(self, value):
        try:
            value.isdigit()
        except:
            raise ValueError("Value Error, phone should contain numbers")
        self.__value = value


class Birthday(Field):
    def __init__(self, value) -> None:
        super().__init__(value)
        self.__value = None
        self.value = value

    @property
    def birthday(self):
        return self.__value

    @birthday.setter
    def birthday(self, value):
        try:
            value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Value Error, please enter day.month.year")
        self.__value = value


class Record:

    def __init__(self, name: Name, num: Phone, bday: Birthday = None) -> None:
        self.name = name
        self.nums = []
        if num:
            self.nums.append(num)

    def add(self, new_num: Phone):
        if new_num.value not in [p.value for p in self.nums]:
            self.nums.append(new_num)
            return new_num

    def remove(self, num: Phone):
        for i, p in enumerate(self.nums):
            if num.value == p.value:
                return self.nums.pop(i)

    def edit(self, num: Phone, new_num: Phone):
        if self.remove(num):
            self.nums.append(new_num)
            return new_num

    def days_to_birthday(self, bday: Birthday):
        if self.bday:
            start = date.today()
            next_bday = datetime.strptime(str(self.bday), '%d.%m.%Y')
            end = date(year=start.year, month=next_bday.month, day=next_bday.day)
            diff = end - start
            return '{:<20}|{:^15}| days till the next Birthday {:>15}s \n'.format(diff)
        return "Birth date not added"

    def __repr__(self):
        return f'{", ".join([p.value for p in self.nums])}'


class AddressBook(UserDict):
    def __init__(self):
        super().__init__()
        self.n = None

        filename = 'database/ab_data'
        dt = self.data

        with shelve.open(filename) as fn:
                fn['dt'] = dt

        with shelve.open(filename) as states:
            for key in states:
                print(f'{key}: {states[key]}')

    def __iter__(self, n):
         self.n = n
         self.count = 0
         return self

    def __next__(self):
        self.count += 1
        if self.count > self.n:
            raise StopIteration
        else:
            for i in self.data:
                yield self.data[i]

    def add_record(self, record: Record):
        self.data[record.name.value] = record


    def find(self, param: str):

        if len(param) < 3:
            raise ValueError("Param for find must be eq or grater then 3 symbols.")

        ab = AddressBook()

        for k, v in self.items():
            if param.lower() in k.lower() or [p.value for p in v.nums if param in p.value]:
                ab.add_record(v)
                continue
        return ab


def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError:
            return "give me 'add' 'name' 'number'"
        except KeyError:
            return "Give me 'name' and 'phone' please"
        except ValueError:
            return "Give me 'change' 'name' 'number'"

    return wrapper


def start_bot():
    return "How can I help you?"


def exit_bot():
    return "Good bye!"


def close_bot():
    return "Good bye!"


def bye_bot():
    return "Good bye!"


data = {}

contacts = {}

ab = AddressBook()


@input_error
def input_add(*args):
    name = Name(args[0])
    phone = Phone(args[1])
    rec = Record(name, phone)
    ab.add_record(rec)
    return f"Contact {args[0].title()} added"


@input_error
def input_change(*args):
    rec = ab.get(args[0])
    if rec:
        phone = Phone(args[1])
        new_phone = Phone(args[2])
        rec.edit(phone, new_phone)
    return f"Contact {args[0].title()} changed"


@input_error
def input_phone(*args):
    rec = ab.get(args[0])
    if rec:
        return rec.phones()


@input_error
def find(*args):
    return ab.find(args[0])


def input_show():
    return "\n".join([f"{v.name.value}: {v.nums} " for v in ab.values()])


COMMANDS = {
    start_bot: "hello",
    input_add: "add",
    input_phone: "phone",
    input_show: "show all",
    input_change: "change",
    exit_bot: "good bye",
    close_bot: "close",
    bye_bot: "exit",
    find: "find"
}


def main():
    while True:
        user_input = input(">>> ")
        if user_input == '.':
            break
        for k, v in COMMANDS.items():
            if user_input.startswith(v):
                cmd, data = k, user_input[len(v):].strip().split()
        print(cmd(*data))


if __name__ == "__main__":
    main()