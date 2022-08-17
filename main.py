import asyncio
import requests
from bs4 import BeautifulSoup

file_name = "song-lyrics.txt"

# Gets every line from song-lyrics.txt
all_lines = []
with open(file_name) as file:
    all_lines = [line.rstrip() for line in file]

# Removes duplicate lines
unique_lines = []
[unique_lines.append(line) for line in all_lines if line not in unique_lines]

# Replaces empty spaces with "+" for url
url_lines = [line.replace(" ", "+") for line in unique_lines]

all_formatted_cards = []


async def get_line_data(url_line):
    print('Getting line data for ' + url_line)
    formatted_cards = []

    r = requests.get("https://ichi.moe/cl/qr/?q=" + url_line + "&r=kana")
    if r.status_code == 200:
        soup = BeautifulSoup(r.content, "html.parser")
        for gloss_row in soup.find_all("div", class_="row gloss-row"):
            for card in gloss_row.find_all("div", class_="gloss"):
                formatted_card = {
                    "title": "",
                    "definitions": [],
                    "pronunciation": ""
                }

                card_title = card.find("dt").text
                card_title_split = card_title.split()
                card_definition = card.find(
                    "ol", class_='gloss-definitions').text
                if card_definition == " ":
                    card_definition = card.find(
                        "div", class_="conjugation").text

                formatted_card["title"] = card_title_split[0]
                formatted_card["definitions"] = card_definition.strip()
                if len(card_title_split) > 1:
                    pro = card_title_split[1]
                    formatted_card["pronunciation"] = pro[1:-1]
                else:
                    formatted_card.pop("pronunciation", None)

                formatted_cards.append(formatted_card)

    for card in formatted_cards:
        if card not in all_formatted_cards:
            all_formatted_cards.append(card)

    print("Done.")
    await asyncio.sleep(.8)


async def main():
    print("Please wait " + str(len(url_lines)) + " seconds")
    for url_line in url_lines:
        await get_line_data(url_line)

    with open('definitions.txt', 'w') as f:
        f.write(str(all_formatted_cards))

asyncio.run(main())
