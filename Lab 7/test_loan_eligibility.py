from hypothesis import given, settings, strategies as st
from loan_eligibility import parse_income, monthly_emi, pan_category, CATEGORIES


# ---------- parse_income ----------

@given(st.text() | st.none())
def test_parse_income_no_crash(s):
    try:
        parse_income(s)
    except Exception as e:
        assert False, f"parse_income crashed with: {e!r}"


@given(st.integers(min_value=0, max_value=10**12))
def test_parse_income_formatted_number(n):
    # 50000 -> "50,000" should come back as 50000
    assert parse_income(f"{n:,}") == n


@given(st.integers(max_value=-1))
def test_parse_income_rejects_negative(n):
    assert parse_income(str(n)) is None


# ---------- monthly_emi ----------

@given(st.text() | st.none())
def test_monthly_emi_no_crash(s):
    try:
        monthly_emi(s)
    except Exception as e:
        assert False, f"monthly_emi crashed with: {e!r}"


@settings(max_examples=300)
@given(st.integers(), st.integers(), st.integers())
def test_monthly_emi_numeric_no_crash(principal, rate, years):
    # well formed "p,r,y" strings with any integers (zero, negative, huge)
    try:
        monthly_emi(f"{principal},{rate},{years}")
    except Exception as e:
        assert False, f"monthly_emi crashed with: {e!r}"


@given(st.integers(min_value=1000, max_value=10**8),
       st.integers(min_value=0, max_value=50),
       st.integers(min_value=1, max_value=30))
def test_monthly_emi_valid_input(principal, rate, years):
    emi = monthly_emi(f"{principal},{rate},{years}")
    assert emi is not None
    assert emi > 0
    # total paid back can never be less than the amount borrowed
    # (small allowance for rounding the EMI to 2 decimals)
    months = years * 12
    assert emi * months >= principal - months * 0.01


# ---------- pan_category ----------

@given(st.text() | st.none())
def test_pan_category_no_crash(s):
    try:
        pan_category(s)
    except Exception as e:
        assert False, f"pan_category crashed with: {e!r}"


@given(st.from_regex(r"[A-Z]{3}[PCHF][A-Z][0-9]{4}[A-Z]", fullmatch=True))
def test_pan_category_valid_pan(pan):
    assert pan_category(pan) == CATEGORIES[pan[3]]
