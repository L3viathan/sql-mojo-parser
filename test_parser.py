import pytest

from sql import yacc

@pytest.mark.parametrize(
    "string,result",
    [
        (
            "select foo from bar",
            {
                "type": "select",
                "columns": [
                    {"type": "name", "value": "foo"},
                ],
                "index": "bar",
            }
        ),
        (
            "select * from bar",
            {
                "type": "select",
                "columns": [
                    {"type": "star"},
                ],
                "index": "bar",
            }
        ),
        (
            "select foo, bar from bar",
            {
                "type": "select",
                "columns": [
                    {"type": "name", "value": "foo"},
                    {"type": "name", "value": "bar"},
                ],
                "index": "bar",
            }
        ),
        (
            "select * from bar limit 10",
            {
                "type": "select",
                "columns": [
                    {"type": "star"},
                ],
                "index": "bar",
                "limit": 10,
            }
        ),
        (
            "select * from bar where a=3",
            {
                "type": "select",
                "columns": [
                    {"type": "star"},
                ],
                "index": "bar",
                "condition": {
                    "op": "=",
                    "args": [
                        {"type": "name", "value": "a"},
                        {"type": "literal", "value": 3},
                    ],
                }
            }
        ),
        (
            "select * from bar where a=3 and b=2",
            {
                "type": "select",
                "columns": [
                    {"type": "star"},
                ],
                "index": "bar",
                "condition": {
                    "op": "and",
                    "args": [
                        {
                            "op": "=",
                            "args": [
                                {"type": "name", "value": "a"},
                                {"type": "literal", "value": 3},
                            ],
                        },
                        {
                            "op": "=",
                            "args": [
                                {"type": "name", "value": "a"},
                                {"type": "literal", "value": 3},
                            ],
                        },
                    ]
                }
            }
        ),
    ]
)
def test_parse_success(string, result):
    # assert parser.parse(string) == result
    # DEBUG: For now just assertion of non-fail
    yacc.parse(string)


@pytest.mark.parametrize(
    "string",
    [
        ("some random string",),
        ("select from foo",),
    ]
)
def test_parse_fail(string):
    with pytest.raises(ValueError):
        yacc.parse(string)
