from src.utils import top_k_similar


def test_top_k_similar():
    target = "apple"
    candidates = ["appl", "apply", "pineapple", "appeal", "applet", "grape", "apple"]

    test_cases = [
        (1, ["apple"]),
        (2, ["apple", "appl"]),
        (3, ["apple", "appl", "apply"]),
        (4, ["apple", "appl", "apply", "applet"]),
        (5, ["apple", "appl", "apply", "applet", "appeal"]),
    ]

    for k, expected in test_cases:
        result = top_k_similar(target=target, candidates=candidates, k=k)
        assert result == expected, f"Failed for k={k}: expected {expected}, got {result}"


if __name__ == "__main__":
    test_top_k_similar()
