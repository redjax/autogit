import pytest


def test_reada_file_contents(txt_file_ex):
    ## Read test file fixture
    with open(txt_file_ex, "r") as f:
        contents = f.read()
    print(f"'{f}' contents: {contents}")
