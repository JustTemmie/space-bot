import fandom
from bs4 import BeautifulSoup
import requests
from libraries.miscLib import str_replacer
from asyncio import run


async def code():
    fandom.set_wiki("Minecraft")

    page = fandom.page(fandom.search("iron ingot")[0][0])

    # print(page.summary)
    # print(page.content["sections"][0])

    # print(page._html)

    soup = BeautifulSoup(page.html, "html.parser")

    # for element in soup:
    #     print(element)

    # for element in soup.find_all("div", class_="notaninfobox"):
    #     result = element.text.strip()

    #     # removes empty lines - https://stackoverflow.com/questions/1140958/whats-a-quick-one-liner-to-remove-empty-lines-from-a-python-string
    #     contents = "".join([s for s in result.splitlines(True) if s.strip("\r\n")])
    #     for i in range(0, 15):
    #         contents = contents.replace("\n", "----", 1)
    #         contents = contents.replace("\n", ": ", 1)
    #     contents = contents.replace("----", "\n")
    #     #contents = await str_replacer(contents, "-", "\n", 2)
    #     print(contents)

    items = []
    for element in soup.find_all("span", class_="sprite inv-sprite"):
        items.append(element.get("title"))

    print(items)

    # summary = fandom.summary(fandom.search("repeater")[0][0], sentences=5)
    # print(summary)


run(code())
