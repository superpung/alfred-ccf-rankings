import json
import os

from src.__main__ import rankings_data, search_results

json_path = os.path.expanduser(rankings_data)
with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

test_cases = [
    ("a", "AI"),
    ("fast", "FAST"),
    ("fse", "FSE"),
]


def test_search_results1():
    for query, output in test_cases:
        result = search_results(query=query, data=data, num=1)
        assert result[0]["entry"]["abbr"] == output
