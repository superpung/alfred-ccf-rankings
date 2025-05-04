#!/usr/bin/python3

import argparse
import json
import os

rankings_data = "src/data/CCF_Ranking_2022.json"
rankings_icon = "assets/rankings/{rank}.png"


def search_results(query):
    categories = {cat["id"]: f"{cat['english']}" for cat in data["category"]}

    searched_results = [
        {"entry": _, "category_name": categories.get(_["category_id"], "")}
        for _ in data["list"]
        if _["abbr"].lower() == query
    ]
    return searched_results


def create_alfred_item(entry, category_name):
    rank_icons = {"A": "", "B": "", "C": ""}
    type_icons = {"Journal": "[Jour]", "Conference": "[Conf]"}

    return {
        "uid": f"{entry['abbr']}-{entry['rank']}",
        "title": f"{rank_icons.get(entry['rank'], '')} {type_icons.get(entry['type'], '')} {entry['name']}",
        "subtitle": f"{entry['abbr']} | {category_name} | {entry['type']} | Ranking: {entry['rank']} | Publisher: {entry.get('publisher', 'N/A')}",
        "arg": entry["name"],
        "text": {
            "copy": f"{entry['name']} ({entry['abbr']}, {entry['rank']})",
            "largetype": f"""📌 {entry["name"]}

Abbr: {entry["abbr"]}
Category: {category_name}
Type: {entry["type"]}
Ranking: {entry["rank"]}
Publisher: {entry.get("publisher", "N/A")}""",
        },
        "quicklookurl": f"https://www.google.com/search?q={entry['name'].replace(' ', '+')}",
        "valid": True,
        "icon": {"path": rankings_icon.format(rank=entry["rank"])},
        "mods": {
            "cmd": {"valid": True, "arg": entry["abbr"], "subtitle": "Copy Abbreviations: " + entry["abbr"]},
            "alt": {
                "valid": True,
                "arg": entry.get("publisher", ""),
                "subtitle": "Copy Publisher: " + entry.get("publisher", "N/A"),
            },
            "ctrl": {"valid": True, "arg": entry["name"], "subtitle": "Search in Google Scholar: " + entry["name"]},
        },
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--name")
    args = parser.parse_args()

    json_path = os.path.expanduser(rankings_data)
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    query = args.name.lower() if args.name else ""

    searched_results = search_results(query=query)

    alfred_items = []
    for result in searched_results[:20]:
        alfred_items.append(create_alfred_item(result["entry"], result["category_name"]))

    if not alfred_items:
        alfred_items.append(
            {
                "title": "No matches found",
                "subtitle": "Try different search terms such as name, acronym or category",
                "valid": False,
            }
        )

    print(json.dumps({"items": alfred_items}, ensure_ascii=False))
