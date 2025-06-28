import pytest
from alter_provinces import Provinator


# Creates test provinces file with given content blocks
# file - the file object to write
# content_blocks - a list of lists of tuples, where each inner list is a block of lines and each tuple is
# an (lhs, rhs) pair representing a line in the block
@pytest.fixture
def province(tmp_path):

    def _create_province(content):
        file_name, content_blocks = content

        file_path = tmp_path / file_name

        with file_path.open('w', encoding='latin-1') as file:
            for block in content_blocks:
                for lhs, rhs in block:
                    file.write(f'{lhs} = {rhs}\n')
                file.write('\n')

        return file_path
    
    return _create_province


@pytest.fixture
def provinator(tmp_path):
    return Provinator(
        provinces_folder = tmp_path,
        province_ids = [
            490
        ],
        patterns_to_search = [("trade_goods", "slaves")],
        new_owner = 'HSS',
        keywords = ["owner", "controller", "add_core", "culture"],
    )


@pytest.mark.parametrize("initial", [
    (
        "42 - Gallifrey.txt",
        [
            [("owner", "Gallifreyans"), ("controller", "Time Lords")]
        ],
    ),
    (
        "490 - Bluh.txt",
        [
            [
                ("owner", "HSS"),
                ("controller", "HSS"),
                ("add_core", "HSS"),
                ("culture", "HSS"),
                ("religion", "Catholic"),
            ],
        ]
    ),
])
def test_should_not_alter(province, provinator, initial):
    file = province(initial)

    with file.open('r', encoding='latin-1') as f:
        old_content = f.read()
        provinator.provinate()

    with file.open('r', encoding='latin-1') as f:
        assert f.read() == old_content


@pytest.mark.parametrize("initial, expected", [
    (
        (
            "490 - Gallifrey.txt",
            [
                [
                    ("owner", "Gallifreyans"),
                    ("controller", "Time Lords"),
                    ("add_core", "Gallifreyans"),
                    ("culture", "Gallifreyan"),
                    ("religion", "None")
                ],
            ]
        ),
        (
            "490 - Gallifrey (1).txt",
            [
                [
                    ("owner", "HSS"),
                    ("controller", "HSS"),
                    ("add_core", "HSS"),
                    ("culture", "HSS"),
                    ("religion", "None"),
                ],
            ]
        ),
    ),
    (
        (
        "42 - Gallifrey.txt",
            [
                [
                    ("owner", "Gallifreyans"),
                    ("controller", "Time Lords"),
                    ("add_core", "Gallifreyans"),
                    ("culture", "Gallifreyan"),
                    ("religion", "None"),
                    ("trade_goods", "slaves"),
                ],
            ]
        ),
        (
            "42 - Gallifrey (1).txt",
            [
                [
                    ("owner", "HSS"),
                    ("controller", "HSS"),
                    ("add_core", "HSS"),
                    ("culture", "HSS"),
                    ("religion", "None"),
                    ("trade_goods", "slaves"),
                ],
            ]
        )
    ),
    (
        (
            "42 - Gallifrey.txt",
            [
                [
                    ("Lord President", "Rassilon"),
                    ("Founder", "Omega"),
                    ("discovered_by", "Gallifreyans"),

                ],
                [
                    ("owner", "Gallifreyans"),
                    ("add_core", "Gallifreyans"),
                    ("culture", "Gallifreyan"),
                    ("religion", "None"),
                    ("trade_goods", "slaves"),
                ],
                [
                    ("discovered_by", "Gallifreyans"),
                ]
            ]
        ),
        (
            "42 - Gallifrey (1).txt",
            [
                [
                    ("Lord President", "Rassilon"),
                    ("Founder", "Omega"),
                    ("discovered_by", "Gallifreyans"),
                    ("controller", "HSS"),
                ],
                [
                    ("owner", "HSS"),
                    ("add_core", "HSS"),
                    ("culture", "HSS"),
                    ("religion", "None"),
                    ("trade_goods", "slaves"),
                ],
                [
                    ("discovered_by", "Gallifreyans"),
                ]
            ]
        ),      
    ),
    (
        (
            "42 - Gallifrey.txt",
            [
                [
                    ("Lord President", "Rassilon"),
                    ("Founder", "Omega"),
                ],
                [
                    ("owner", "Gallifreyans"),
                    ("controller", "Time Lords"),
                    ("add_core", "Gallifreyans"),
                    ("culture", "Gallifreyan"),
                    ("religion", "None"),
                    ("trade_goods", "slaves"),
                    ("discovered_by", "Gallifreyans"),
                ],
                [
                    ("discovered_by", "Gallifreyans"),
                ]
            ]
        ),
        (
              "42 - Gallifrey (1).txt",
            [
                [
                    ("Lord President", "Rassilon"),
                    ("Founder", "Omega"),
                ],
                [
                    ("owner", "HSS"),
                    ("controller", "HSS"),
                    ("add_core", "HSS"),
                    ("culture", "HSS"),
                    ("religion", "None"),
                    ("trade_goods", "slaves"),
                    ("discovered_by", "Gallifreyans"),
                ],
                [
                    ("discovered_by", "Gallifreyans"),
                ]
            ]
        ),   
    ),
    (
        (
            "42 - Gallifrey.txt",
            [
                [
                    ("trade_goods", "slaves"),
                ],
                [
                    ("discovered_by", "Gallifreyans"),
                    ("clip", "clop"),
                ]
            ]
        ),
        (
            "42 - Gallifrey (1).txt",
            [
                [
                    ("trade_goods", "slaves"),
                ],
                [
                    ("discovered_by", "Gallifreyans"),
                    ("clip", "clop"),
                    ("owner", "HSS"),
                    ("controller", "HSS"),
                    ("add_core", "HSS"),
                    ("culture", "HSS"),
                ]
            ]
        ),
    ),
], ids=['1', '2', '3', '4', '5'])
def test_should_alter(province, provinator, initial, expected):
        initial_file = province(initial)
        provinator.provinate()
        expected_file = province(expected)

        with initial_file.open('r', encoding='latin-1') as f:
            altered_content = f.read()

        with expected_file.open('r', encoding='latin-1') as f:
            expected_content = f.read()
        
        assert altered_content == expected_content
