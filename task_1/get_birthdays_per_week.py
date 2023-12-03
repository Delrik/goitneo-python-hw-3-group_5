from collections import defaultdict
import datetime


def is_valid_entry(user) -> bool:
    return user["name"] and user["birthday"]


def get_birthdays_per_week(users):
    result = defaultdict(list)
    current_date = datetime.datetime.now()
    for user in users:
        if not is_valid_entry(user):
            print("Invalid entry: ", user)
        else:
            user_birthday = user["birthday"].date()
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
                result[date_name].append(user["name"])
    for day, names in result.items():
        print(f"{day}: {', '.join(names)}")
