#!/usr/bin/env python3
# -*- coding: utf-8 -*-

WIERSZE_PATHNAME = "/home/beniamin/Documents/wiersze.md"
CONNECTOR = "%"


class Poem:
    def __init__(self, title: str):
        self.title = title.strip()
        self.vrss = []
        self.vrs_len = 4

    def __str__(self):
        res = "TITLE:\n" + self.title + "TEKST:\n"
        for wers in self.vrss:
            res += wers
        return res

    def to_anki(self):
        vrss = [
            self.vrss[i : i + self.vrs_len]
            for i in range(0, len(self.vrss), self.vrs_len)
        ]
        wersy = [self.title]
        wersy += [("<br/>".join(wers)).strip() for wers in vrss]
        wersy += ["KONIEC"]

        for idx, _ in enumerate(wersy[:-1]):
            print("{} {} {}".format(wersy[idx], CONNECTOR, wersy[idx + 1]))


def main():
    with open(WIERSZE_PATHNAME, "r", encoding="utf-8") as f:
        poems = []
        for line in f:
            if line.startswith("##"):
                title = line.replace("##", "")
                poems.append(Poem(title))
            elif line.isspace() or line.strip() == "[...]":
                pass
            else:
                poems[-1].vrss.append(line.strip())

        for wiersz in poems:
            # print("Wiersz: {:d}".format(idx + 1))
            wiersz.to_anki()


if __name__ == "__main__":
    main()
