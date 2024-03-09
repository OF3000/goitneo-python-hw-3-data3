from datetime import datetime, timedelta
from collections import defaultdict


def get_birthdays_per_week(users):
    today = datetime.today().date()
    # today=datetime(2024,3,11).date()
    bd = defaultdict(list)

    tw = today.weekday()
    for user in users:
        name = user["name"]
        birthday = user["birthday"].date()
        birthday_this_year = birthday.replace(year=today.year)
        if birthday_this_year < today:
            birthday_this_year.replace(year=today.year + 1)
        delta_days = (birthday_this_year - today).days
        if tw - 2 <= delta_days < 7:
            # print(birthday_this_year)
            bw = birthday_this_year.strftime("%A")
            if bw in ("Saturday", "Sunday") and birthday_this_year < today:
                bw = "Monday"
            elif bw in ("Saturday", "Sunday") and birthday_this_year > today:
                continue
            elif birthday_this_year < today:
                continue
            bd[bw].append(name)

    if len(bd) > 0:
        for i in range(7):
            tw = (today + timedelta(days=i)).strftime("%A")
            if not bd[tw]:
                continue
            s = ", ".join(bd[tw])
            print(f"{tw}: {s}")
    else:
        print("No more Birthdays this week")


if __name__ == "__main__":
    users = [
        {"name": "Bill Gates", "birthday": datetime(1955, 1, 28)},
        {"name": "Jimm Gates", "birthday": datetime(1955, 2, 28)},
        {"name": "John Gates", "birthday": datetime(1955, 2, 25)},
        {"name": "Tom Gates", "birthday": datetime(1955, 2, 26)},
        {"name": "Ben Gates", "birthday": datetime(1955, 3, 2)},
        {"name": "Peter Gates", "birthday": datetime(1955, 3, 3)},
    ]

    get_birthdays_per_week(users)
