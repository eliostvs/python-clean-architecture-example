import inspect
from os.path import dirname, abspath, join

from click.testing import CliRunner

from example.cli.controller import run

HERE = dirname(abspath(__file__))

success_response = """
4 - Ian Kehoe
5 - Nora Dempsey
6 - Theresa Enright
8 - Eoin Ahearn
11 - Richard Finnegan
12 - Christina McArdle
13 - Olive Ahearn
15 - Michael Ahearn
17 - Patricia Cahill
23 - Eoin Gallagher
24 - Rose Enright
26 - Stephen McArdle
29 - Oliver Ahearn
30 - Nick Enright
31 - Alan Behan
39 - Lisa Ahearn
"""


def test_integration_succeed():
    runner = CliRunner()
    result = runner.invoke(run, [join(HERE, "customers.txt")])

    assert result.exit_code == 0
    assert result.output.strip() == inspect.cleandoc(success_response)


def test_integration_fail():
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open("invalid-file.txt", "w") as f:
            f.write("Hello World!")

        result = runner.invoke(run, ["invalid-file.txt"])
        assert result.exit_code == 0
        assert result.output == "Invalid json\n"
