import pytest

from loan_eligibility import credit_band, interest_rate, is_eligible


def test_credit_band_returns_each_band():
    assert credit_band(800) == "excellent"
    assert credit_band(700) == "good"
    assert credit_band(600) == "fair"
    assert credit_band(500) == "poor"


def test_credit_band_rejects_scores_outside_valid_range():
    with pytest.raises(ValueError, match="invalid score"):
        credit_band(299)

    with pytest.raises(ValueError, match="invalid score"):
        credit_band(901)


def test_eligible_applicant():
    assert is_eligible(30, 50000, "salaried", 800) is True


def test_ineligible_applicant_for_age():
    assert is_eligible(20, 50000, "salaried", 800) is False


def test_ineligible_applicant_for_income():
    assert is_eligible(30, 24999, "salaried", 800) is False


def test_ineligible_applicant_for_poor_credit():
    assert is_eligible(30, 50000, "salaried", 500) is False


def test_unknown_employment_is_rejected():
    with pytest.raises(ValueError, match="unknown employment"):
        is_eligible(30, 50000, "contractor", 800)


def test_interest_rate_for_each_credit_band():
    assert interest_rate(800, "salaried", False) == 8
    assert interest_rate(700, "salaried", False) == 10
    assert interest_rate(600, "salaried", False) == 13


def test_interest_rate_adjustments():
    assert interest_rate(800, "self_employed", True) == 7
