#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re


class Word(dict):
    LINE_PATTERN_STR = r"^(.+?) - (.+) ; (.*) / (.*)$"
    LINE_PATTERN = re.compile(LINE_PATTERN_STR)

    def __init__(self, word: str, pl: str, eng: str, sent: str):
        super().__init__()
        self.word = word
        self.pl = pl
        self.eng = eng
        self.sent = sent

    def __setattr__(self, key, value):
        self[key] = value

    def __getattr__(self, attr):
        return self[attr]

    @staticmethod
    def from_line(line: str):
        m = re.fullmatch(Word.LINE_PATTERN, line.strip())

        if not m:
            return None

        word, pl, eng, sent = m.groups()
        return Word(word, pl, eng, sent)

    def __str__(self):
        return f'{self["word"]} - {self["pl"]} ; {self["eng"]} / {self["sent"]}'
