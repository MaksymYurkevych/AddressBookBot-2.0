import re

from decorators import error_handler
from class_part import *

HELP_INSTRUCTIONS = """This contact bot save your contacts 
    Global commands:
      'add contact' - add new contact. Input user name and phone
    Example: add User_name 095-xxx-xx-xx
      'add birthday' - add birthday of some User. Input user name and birthday in format yyyy-mm-dd
    Example: add User_name 1971-01-01
      'change' - change users old phone to new phone. Input user name, old phone and new phone
    Example: change User_name 095-xxx-xx-xx 050-xxx-xx-xx
      'delete contact' - delete contact (name and phones). Input user name
    Example: delete contact User_name
      'delete phone' - delete phone of some User. Input user name and phone
    Example: delete phone User_name 099-xxx-xx-xx
      'phone' - show contacts of input user. Input user name
    Example: phone User_name
      'show all' - show all contacts
    Example: show all
      'show list' - show list of contacts which contains N-users
    Example: show list 5 
      'when birthday' - show days to birthday of User/ Input user name
    Example: when celebrate User_name
      'exit/'.'/'bye'/'good bye'/'close' - exit bot
    Example: good bye"""


@error_handler
def add_phone(*args):
    """Adds new contact, requires name and phone"""
    name = Name(args[0])
    phone = Phone(args[1])
    rec = ADDRESSBOOK.get(name.value)

    if name.value in ADDRESSBOOK.show_all_records():
        while True:
            user_input = input(
                "Contact with this name already exist, do you want to rewrite it or create new record? '1'/'2'\n")
            if user_input == "2":
                name.value += "(1)"
                rec = ADDRESSBOOK.get(name.value)
                break
            elif user_input == "1":
                ADDRESSBOOK.remove_record(rec)
                rec = ADDRESSBOOK.get(name.value)
                break
            else:
                print("Please type '1' or '2' to continue")

    if not phone.value.isnumeric():
        raise ValueError
    if rec:
        rec.add_phone(phone)
    else:
        rec = Record(name, phone)
        ADDRESSBOOK.add_record(rec)
    return f'You just added contact "{name}" with phone "{phone}" to your list of contacts'


@error_handler
def hello(*args):
    """Greets user"""
    return "How can I help you?"


@error_handler
def change(*args):
    """Replace phone number for an existing contact"""
    name = Name(args[0])
    old_ph = Phone(args[1])
    new_ph = Phone(args[2])

    if not new_ph.value.isnumeric():
        raise ValueError

    ADDRESSBOOK.change_record(name.value, old_ph.value, new_ph.value)
    return f"You just changed number for contact '{name}'. New number is '{new_ph}'"


@error_handler
def phone(*args):
    """Shows a phone number for a chosen contact"""
    return ADDRESSBOOK.show_one_record(args[0])


@error_handler
def helper(*args):
    return HELP_INSTRUCTIONS


@error_handler
def delete_contact(*args):
    name = Name(args[0])
    rec = Record(name)
    if name.value:
        ADDRESSBOOK.remove_record(rec)
        return f"{name} was deleted from your contact list"
    else:
        raise IndexError


@error_handler
def add_birthday(*args):
    name = Name(args[0])
    birthday = tuple(re.split('\D', args[1]))

    if "" in birthday or len(birthday) != 3:
        return "Date is not correct. Please write date in format: yyyy-m-d"

    if name.value in ADDRESSBOOK:
        ADDRESSBOOK[name.value].add_birthday(*birthday)
        return f"The birthday for {name.value} was added"
    return f"{name.value} is not in your contact list"


@error_handler
def days_to_birthday(*args):
    name = Name(args[0])
    if name.value in ADDRESSBOOK:
        if ADDRESSBOOK[name.value].birthday:
            days = ADDRESSBOOK[name.value].days_to_birthday()
            return days
        return f"{name.value}'s birthday is not set"
    else:
        raise KeyError


@error_handler
def delete_phone(*args):
    name = Name(args[0])
    phone = Phone(args[1])
    if name.value in ADDRESSBOOK:
        ADDRESSBOOK[name.value].remove_phone(phone.value)
        return f"Phone for {name.value} was deleted"
    return f"Contact {name.value} does not exist"


@error_handler
def show_all(*args):
    """Show a list of all contacts that were added before"""
    if len(ADDRESSBOOK) > 0:
        return ADDRESSBOOK.show_all_records()
    return "Your addressbook is empty"


@error_handler
def show_list(*args):
    if len(ADDRESSBOOK):
        return "".join(ADDRESSBOOK.iterator(int(args[0])))
    return "Your address book is empty"


COMMANDS = {
    show_list: "show list",
    delete_phone: "delete phone",
    days_to_birthday: "when birthday",
    add_birthday: "add birthday",
    add_phone: "add contact",
    hello: "hello",
    show_all: "show all",
    change: "change",
    phone: "phone",
    helper: "help",
    delete_contact: "delete contact"
}


def command_parser(user_input):
    for command, key_word in COMMANDS.items():
        if user_input.startswith(key_word):
            return command, user_input.replace(key_word, "").strip().split(" ")
    return None, None


def main():
    print(
        "Here's a list of available commands: 'Hello', 'Add contact', 'Add birthday', 'When birthday', "
        "'Delete contact', 'Change', 'Phone', 'Show all', 'Delete phone', 'Help', 'Exit'")
    while True:
        user_input = input(">>>")
        end_words = [".", "close", "bye", "exit"]

        if user_input.lower() in end_words:
            print("Goodbye and good luck")
            break

        command, data = command_parser(user_input.lower())

        if not command:
            print("Sorry, unknown command")
        else:
            print(command(*data))


if __name__ == '__main__':

    main()
