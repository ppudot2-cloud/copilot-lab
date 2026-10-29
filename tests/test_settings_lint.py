from solutionops.settings_lint import lint_settings


def test_valid_settings_have_no_issues():
    data = {"EnvironmentVariables": [], "ConnectionReferences": []}
    assert lint_settings(data, "dev") == []


def test_missing_key_is_reported():
    issues = lint_settings({"EnvironmentVariables": []}, "uat")
    assert [i.rule for i in issues] == ["missing-key"]


def test_wrong_type_is_reported():
    issues = lint_settings({"EnvironmentVariables": {}, "ConnectionReferences": []}, "dev")
    assert [i.rule for i in issues] == ["bad-type"]
