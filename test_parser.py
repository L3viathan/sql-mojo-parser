import pytest

from sql_mojo_parser import yacc

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
                "index": {"type": "name", "value": "bar"},
            }
        ),
        (
            "select * from bar",
            {
                "type": "select",
                "columns": [
                    {"type": "star"},
                ],
                "index": {"type": "name", "value": "bar"},
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
                "index": {"type": "name", "value": "bar"},
            }
        ),
        (
            "select * from bar limit 10",
            {
                "type": "select",
                "columns": [
                    {"type": "star"},
                ],
                "index": {"type": "name", "value": "bar"},
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
                "index": {"type": "name", "value": "bar"},
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
                "index": {"type": "name", "value": "bar"},
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
                                {"type": "name", "value": "b"},
                                {"type": "literal", "value": 2},
                            ],
                        },
                    ]
                }
            }
        ),
        (
            "select * from bar where a=3 and (b=2 or c=1)",
            {
                "type": "select",
                "columns": [
                    {"type": "star"},
                ],
                "index": {"type": "name", "value": "bar"},
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
                            "op": "or",
                            "args": [
                                {
                                    "op": "=",
                                    "args": [
                                        {"type": "name", "value": "b"},
                                        {"type": "literal", "value": 2},
                                    ],
                                },
                                {
                                    "op": "=",
                                    "args": [
                                        {"type": "name", "value": "c"},
                                        {"type": "literal", "value": 1},
                                    ],
                                },
                            ],
                        },
                    ],
                },
            },
        ),
        (
            "select * from bar where a=3 and b=2 or c=1",
            {
                "type": "select",
                "columns": [
                    {"type": "star"},
                ],
                "index": {"type": "name", "value": "bar"},
                "condition": {
                    "op": "or",
                    "args": [
                        {
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
                                        {"type": "name", "value": "b"},
                                        {"type": "literal", "value": 2},
                                    ],
                                },
                            ],
                        },
                        {
                            "op": "=",
                            "args": [
                                {"type": "name", "value": "c"},
                                {"type": "literal", "value": 1},
                            ],
                        },
                    ],
                },
            },
        ),
    ]
)
def test_parse_success(string, result):
    assert yacc.parse(string) == result


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
