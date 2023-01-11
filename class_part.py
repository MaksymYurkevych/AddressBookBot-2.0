from collections import UserDict
from datetime import datetime


class Field:
    """Parent class for all fields"""

    def __init__(self, value):
        self.__value = None
        self.value = value

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value


class Name(Field):
    """Required field with username"""

    pass

    # def __str__(self):
    #     return self._value

    # def __repr__(self):
    #     return self._value

    # # @Field.value.setter
    # # def value(self, value):
    # #     self._value = value


class Phone(Field):
    """Optional field with phone numbers"""

    # def __init__(self, value):
    #     super().__init__(value)
    #     self._value = Phone.sanitize_number(value)

    # def __str__(self):
    #     return self._value

    # @staticmethod
    # def sanitize_number(number):
    #     """Return phone number that only include digits"""
    #     clean_phone = (
    #         number.strip()
    #         .replace("-", "")
    #         .replace("(", "")
    #         .replace(")", "")
    #         .replace("+", "")
    #     )
    #     return clean_phone

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value  # Phone.sanitize_number(value)  # ?????


class Birthday(Field):
    """Creating 'birthday' fields"""

    # def __init__(self, year, month, day):
    #     self.__birthday = self.sanitize_birthday_date(year, month, day)

    # def __str__(self):
    #     return str(self.__value)

    # def __repr__(self):
    #     return str(self.__value)

    # @staticmethod
    # def sanitize_birthday_date(year, month, day):
    #     birthday = datetime(year=year, month=month, day=day)
    #     return str(birthday.date())

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        try:
            self.__value = datetime.strptime(value, "%d-%m-%Y").date()
        except ValueError:
            raise ValueError('Birthdate must be in "DD-MM-YYYY" format')

    def __str__(self):
        return self.value.strftime("%d-%m-%Y")

    def __repr__(self):
        return str(self)


class Record:
    """Class for add, remove, change fields"""

    def __init__(self, name: Name, phone: Phone = None, birthday: Birthday = None):

        # if birthday:
        #     self.birthday = Birthday(*birthday)
        # else:
        #     self.birthday = None
        self.name = name
        # self.phone = phone навіщо це?
        self.phones = []
        if phone:
            self.phones.append(phone)
        self.birthday = birthday

    def add_phone(self, phone: Phone):
        self.phones.append(phone)
        return f"phone {phone} add successful"

    # TODO change func is not working if old number is incorrect
    def change(self, old_phone: Phone, new_phone: Phone):
        for phone in self.phones:
            if (
                phone.value == old_phone.value
            ):  # можливо реалізувати метод __eq__ і буде більш наглядно
                self.phones.remove(phone)
                self.phones.append(new_phone)
                return f"Phone {old_phone} change successful on phone {new_phone}"
        return f"Phone number '{old_phone}' was not found in the record"

    def add_birthday(self, birthday: Birthday):
        # self.birthday = Birthday.sanitize_birthday_date(int(year), int(month), int(day))
        self.birthday = birthday

    def days_to_birthday(self):

        cur_date = datetime.now().date()
        cur_year = cur_date.year

        if self.birthday:
            bd = self.birthday.value
            # birthday = datetime.strptime(self.birthday, "%Y-%m-%d")
            this_year_birthday = bd.replace(
                year=cur_year
            )  # datetime(cur_year, birthday.month, birthday.day).date()
            delta = (this_year_birthday - cur_date).days
            if delta >= 0:
                return f"{self.name}'s birthday will be in {delta} days"
            else:
                # next_year_birthday = datetime(
                #     cur_year + 1, birthday.month, birthday.day
                # ).date()
                next_year_birthday = this_year_birthday.replace(year=cur_year + 1)
                delta = (next_year_birthday - cur_date).days
                return f"{self.name}'s birthday will be in {delta} days"
        else:
            return f"{self.name}'s birthday is unknown"

    def show_contact_info(self):
        phones = ", ".join([str(ph) for ph in self.phones])
        return {
            "name": str(self.name.value),
            "phone": phones,
            "birthday": self.birthday,
        }

    def remove_phone(self, phone):
        phone = Phone(phone)
        for ph in self.phones:
            if ph.value == phone.value:
                self.phones.remove(ph)
        return f"Number {phone} not found"

    def __str__(self) -> str:
        return f'name: {self.name} {", ".join([str(p) for p in self.phones])} {"birthday: " + str(self.birthday) if self.birthday else ""}'

    def __repr__(self) -> str:
        return str(self)


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
            f"Name: {rec.name}; Birthday: {rec.birthday}; Phone: {', '.join([ph.value for ph in rec.phones])}"
            for rec in self.data.values()
        )

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


if __name__ == "__main__":
    ab = AddressBook()
    rec1 = Record(Name("Bill"), Phone("1234567890"))
    print(rec1)
    try:
        rec2 = Record(Name("Jill"), Phone("0987654321"), Birthday("12.03.1995"))
    except ValueError as e:
        print(e)
    rec2 = Record(Name("Jill"), Phone("0987654321"), Birthday("12-03-1995"))
    print(rec2)
    ab.add_record(rec1)
    ab.add_record(rec2)
    print(ab)

    phone3 = Phone("7893453434")
    print(phone3)
    rec1.add_phone(phone3)

    print(ab)

    bd = Birthday("25-04-1986")

    rec1.add_birthday(bd)

    phone4 = Phone("7893453434")  # такий самий, як phone3, але це інший інстанс

    phone5 = Phone("0667899999")

    print(rec1.change(phone4, phone5))

    print(ab)

    print(ab.get("Bill").days_to_birthday())
    print(ab.get("Jill").days_to_birthday())
