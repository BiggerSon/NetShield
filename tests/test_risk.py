from app.risk import severity_from_score


def test_low():

    assert severity_from_score(10) == "LOW"


def test_medium():

    assert severity_from_score(50) == "MEDIUM"


def test_high():

    assert severity_from_score(75) == "HIGH"


def test_critical():

    assert severity_from_score(95) == "CRITICAL"