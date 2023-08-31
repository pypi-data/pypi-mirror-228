################################################################################
#                                 py-fast-trie                                 #
#          Python library for tries with different grades of fastness          #
#                       (C) 2020, 2022-2023 Jeremy Brown                       #
#                Released under Prosperity Public License 3.0.0                #
################################################################################

from hypothesis import HealthCheck, settings
from hypothesis.database import ExampleDatabase


settings.register_profile(
    "ci",
    database=ExampleDatabase(":memory:"),
    deadline=None,
    max_examples=500,
    stateful_step_count=300,
    suppress_health_check=[HealthCheck.too_slow],
)
