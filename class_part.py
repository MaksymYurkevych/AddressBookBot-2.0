from collections import UserDict
from datetime import datetime


class Field:
    """Parent class for all fields"""

    def __init__(self, value):
        self._value = value

    def __str__(self):
        return self._value

    def __repr__(self):
        return self._value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value


class Name(Field):
    """Required field with username"""

    def __str__(self):
        return self._value

    def __repr__(self):
        return self._value

    @Field.value.setter
    def value(self, value):
        self._value = value


class Phone(Field):
    """Optional field with phone numbers"""

    def __init__(self, value):
        super().__init__(value)
        self._value = Phone.sanitize_number(value)

    def __str__(self):
        return self._value

    @staticmethod
    def sanitize_number(number):
        """Return phone number that only include digits"""
        clean_phone = (number.strip().replace("-", "").replace("(", "").replace(")", "").replace("+", ""))
        return clean_phone

    @property
    def value(self):
        return self._value

    @Field.value.setter
    def value(self, value):
        self._value = Phone.sanitize_number(value)


class Birthday(datetime):
    """Creating 'birthday' fields"""

    def __init__(self, year, month, day):
        self.__birthday = self.sanitize_birthday_date(year, month, day)

    def __str__(self):
        return str(self.__birthday)

    def __repr__(self):
        return str(self.__birthday)

    @staticmethod
    def sanitize_birthday_date(year, month, day):
        birthday = datetime(year=year, month=month, day=day)
        return str(birthday.date())

    @property
    def birthday(self):
        return self.__birthday

    @birthday.setter
    def birthday(self, year, month, day):
        self.__birthday = self.sanitize_birthday_date(year, month, day)


class Record:
    """Class for add, remove, change fields"""

    def __init__(self, name: Name, phone: Phone = None, birthday=None):

        if birthday:
            self.birthday = Birthday(*birthday)
        else:
            self.birthday = None
        self.name = name
        self.phone = phone
        self.phones = []
        if phone:
            self.phones.append(phone)

    def add_phone(self, phone):
        self.phones.append(phone)

    # TODO change func is not working if old number is incorrect
    def change(self, old_phone, new_phone):
        for phone in self.phones:
            if phone == old_phone:
                self.phones.remove(phone)
                self.phones.append(new_phone)
                return
            return f"Phone number '{old_phone}' was not found in the record"

    def add_birthday(self, year, month, day):
        self.birthday = Birthday.sanitize_birthday_date(int(year), int(month), int(day))

    def days_to_birthday(self):

        cur_date = datetime.now().date()
        cur_year = cur_date.year

        if self.birthday:
            birthday = datetime.strptime(self.birthday, '%Y-%m-%d')
            this_year_birthday = datetime(cur_year, birthday.month, birthday.day).date()
            delta = this_year_birthday - cur_date
            if delta.days >= 0:
                return f"{self.name}'s birthday will be in {delta.days} days"
            else:
                next_year_birthday = datetime(cur_year + 1, birthday.month, birthday.day).date()
                delta = next_year_birthday - cur_date
                return f"{self.name}'s birthday will be in {delta.days} days"
        else:
            return f"{self.name}'s birthday is unknown"

    def show_contact_info(self):
        phones = ", ".join([str(ph) for ph in self.phones])
        return {
            "name": str(self.name.value),
            "phone": phones,
            "birthday": self.birthday
        }

    def remove_phone(self, phone):
        phone = Phone(phone)
        for ph in self.phones:
            if ph.value == phone.value:
                self.phones.remove(ph)
        return f"Number {phone} not found"


class AddressBook(UserDict):
    """Class for creating address book"""

    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def remove_record(self, record):
        self.data.pop(record.name.value, None)

    def show_one_record(self, name):
        return f"Name: {name}; Birthday: {self.data[name].birthday}; Phone: {', '.join([str(phone.value) for phone in self.data[name].phones])}"

    def show_all_records(self):
        return "\n".join(
            f"Name: {rec.name}; Birthday: {rec.birthday}; Phone: {', '.join([ph.value for ph in rec.phones])}" for rec
            in self.data.values())

    def change_record(self, username, old_n, new_n):
        record = self.data.get(username)
        if record:
            record.change(old_n, new_n)

    def iterator(self, n):
        records = list(self.data.keys())
        records_num = len(records)
        count = 0
        result = ""
        if n > records_num:
            n = records_num
        for rec in self.data.values():
            if count < n:
                result += f'{rec.name} (B-day: {rec.birthday}): {", ".join([p.value for p in rec.phones])}\n'
                count += 1
        yield result


ADDRESSBOOK = AddressBook()
