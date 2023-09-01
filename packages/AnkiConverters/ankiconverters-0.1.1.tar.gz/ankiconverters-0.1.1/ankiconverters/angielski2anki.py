#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os.path
import sys
from angielski_word import Word


def convert_word(wrd):
    return f"{wrd.word} <br><br> {wrd.sent} ; {wrd.pl} <br><br> {wrd.eng}"


def main():
    input_path = (
        sys.argv[1]
        if len(sys.argv) > 1
        else os.path.expanduser("~/Documents/angielski")
    )
    with open(os.path.expanduser(input_path), encoding="utf-8") as f, open(
        os.path.expanduser("anki_angielski.txt"), "w", encoding="utf-8"
    ) as f_out:
        for line in f:
            word = Word.from_line(line)
            assert word is not None

            anki_word = convert_word(word)

            f_out.write(anki_word)
            f_out.write("\n")


if __name__ == "__main__":
    main()
