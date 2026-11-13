import re

CATEGORIES = {"P": "Individual", "C": "Company", "H": "HUF", "F": "Firm"}

# only plain ASCII digits; str.isdigit() also accepts things like '²' which int() rejects
DIGITS = re.compile(r"[0-9]+")
PAN_FORMAT = re.compile(r"[A-Z]{5}[0-9]{4}[A-Z]")

MAX_DIGITS = 15        # keeps int() away from huge strings
MAX_RATE = 100         # annual interest rate in percent
MAX_YEARS = 50


def _to_int(text):
    """Return a non-negative int for a string of digits, otherwise None."""
    text = text.strip()
    if not DIGITS.fullmatch(text) or len(text) > MAX_DIGITS:
        return None
    return int(text)


def parse_income(income):
    if not isinstance(income, str):
        return None
    return _to_int(income.replace(',', ''))


def monthly_emi(details):
    if not isinstance(details, str):
        return None
    parts = details.split(',')
    if len(parts) != 3:
        return None

    principal, rate, years = (_to_int(p) for p in parts)
    if principal is None or rate is None or years is None:
        return None
    if principal <= 0 or rate > MAX_RATE or not 1 <= years <= MAX_YEARS:
        return None

    n = years * 12
    if rate == 0:
        # no interest: the formula below would divide by zero
        return round(principal / n, 2)

    r = rate / 1200
    growth = (1 + r) ** n
    return round(principal * r * growth / (growth - 1), 2)


def pan_category(pan):
    if not isinstance(pan, str):
        return None
    pan = pan.strip().upper()
    if not PAN_FORMAT.fullmatch(pan):
        return None
    return CATEGORIES.get(pan[3])


def main():
    print("==== Running parse_income ====")
    user_input = input("Enter monthly income (e.g. 50,000): ")
    result = parse_income(user_input)
    print("Income:", result if result is not None else "Invalid income")

    print("\n==== Running monthly_emi ====")
    user_input = input("Enter principal,rate,years (e.g. 500000,10,5): ")
    result = monthly_emi(user_input)
    print("Monthly EMI:", result if result is not None else "Invalid loan details")

    print("\n==== Running pan_category ====")
    user_input = input("Enter a PAN number (e.g. ABCPE1234F): ")
    result = pan_category(user_input)
    print("PAN Category:", result if result is not None else "Invalid PAN")


if __name__ == "__main__":
    main()
