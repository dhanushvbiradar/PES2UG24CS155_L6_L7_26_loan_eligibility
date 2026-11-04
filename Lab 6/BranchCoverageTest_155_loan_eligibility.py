import pytest

from loan_eligibility import credit_band, interest_rate, is_eligible


@pytest.mark.parametrize(
    ("score", "expected"),
    [
        (299, "invalid"),
        (300, "poor"),
        (549, "poor"),
        (550, "fair"),
        (649, "fair"),
        (650, "good"),
        (749, "good"),
        (750, "excellent"),
        (900, "excellent"),
        (901, "invalid"),
    ],
)
def test_credit_band_boundaries(score, expected):
    if expected == "invalid":
        with pytest.raises(ValueError, match="invalid score"):
            credit_band(score)
    else:
        assert credit_band(score) == expected


@pytest.mark.parametrize(
    ("age", "income", "employment", "score", "expected"),
    [
        (20, 50000, "salaried", 800, False),
        (61, 50000, "salaried", 800, False),
        (21, 24999, "salaried", 800, False),
        (60, 39999, "self_employed", 800, False),
        (21, 25000, "salaried", 550, True),
        (60, 40000, "self_employed", 650, True),
        (30, 50000, "salaried", 549, False),
    ],
)
def test_eligibility_decision_branches(
    age, income, employment, score, expected
):
    assert is_eligible(age, income, employment, score) is expected


def test_eligibility_rejects_unknown_employment():
    with pytest.raises(ValueError, match="unknown employment"):
        is_eligible(30, 50000, "contractor", 800)


@pytest.mark.parametrize(
    ("score", "employment", "has_collateral", "expected"),
    [
        (800, "salaried", False, 8),
        (700, "salaried", True, 8),
        (600, "self_employed", False, 14),
        (500, "self_employed", True, 12),
    ],
)
def test_interest_rate_adjustment_branches(
    score, employment, has_collateral, expected
):
    assert interest_rate(score, employment, has_collateral) == expected
