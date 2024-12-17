# -*- coding: utf-8 -*-
"""Basic test suite."""

import __future__  # noqa: F401

from os import listdir, path
from typing import Generator, Tuple

from bs4 import BeautifulSoup
from pytest import raises

from kindle_to_markdown import __main__ as main
from kindle_to_markdown.__main__ import NoteHeading
from kindle_to_markdown.languages import SUPPORTED_LANGUAGES


class TestCode:  # noqa: D101

    def test_extract_note_heading(self) -> None:  # noqa: D102
        test_case: Tuple[str, NoteHeading]
        for test_case in [
            (
                'Markierung(gelb) - Seite 61 · Position 596',
                NoteHeading('textmark', '61', '596', None),
            ),
            (
                'Markierung(gelb) - 8. Frag – aber > Seite 184 · Position 2304',
                NoteHeading('textmark', '184', '2304', '8. Frag - aber'),
            ),
            (
                'Markierung(gelb) - Seite 99 · Position 652',
                NoteHeading('textmark', '99', '652', None),
            ),
            (
                'Markierung(gelb) - Seite 28 · Position 407',
                NoteHeading('textmark', '28', '407', None),
            ),
            (
                'Markierung(gelb) - Seite 229 · Position 3061',
                NoteHeading('textmark', '229', '3061', None),
            ),
            (
                'Markierung(gelb) - RESISTANCE IS\n     INTERNAL > Position 148',
                NoteHeading('textmark', None, '148', 'RESISTANCE IS INTERNAL'),
            ),
            (
                'Markierung(gelb) - Position 79',
                NoteHeading('textmark', None, '79', None),
            ),
            (
                'Notiz - 5: Obsess Over Quality > Seite 175 · Position 2127',
                NoteHeading('note', '175', '2127', '5: Obsess Over Quality'),
            ),
            (
                'Markierung(gelb) - Seite xi · Position 68',
                NoteHeading('textmark', 'xi', '68', None),
            ),
            (
                'Markierung(gelb) - Chapter 1: The Matching Principle: How to Fail at Recruiting Spies > Seite 8 · Position 268',  # noqa: E501
                NoteHeading(
                    'textmark',
                    '8',
                    '268',
                    'Chapter 1: The Matching Principle: How to Fail at Recruiting Spies',  # noqa: E501
                ),
            ),
        ]:
            results = main.extract_note_heading(test_case[0], SUPPORTED_LANGUAGES['de'])
            assert test_case[1] == results

    def test_extract_annotations(self) -> None:  # noqa: D102
        for fixture in self.__get_test_fixtures():
            with open(fixture[1], 'r') as i_fh:
                soup = BeautifulSoup(i_fh, 'html.parser')

            output = main.extract_annotations(soup, SUPPORTED_LANGUAGES.get(fixture[0]))
            assert output == [
                '# Basti Tee - My ebook\n',
                '## First section\n',
                '> 🔖 p. 5, pos. 28\n',
                'A marked text. (p. 5, pos. 35)\n',
                'More marked text. (p. 6, pos. 44)\n',
                '> Personal note. (p. 6, pos. 44)\n',
                '> Note without text. (p. 6, pos. 49)\n',
            ]

    def test_guess_language(self) -> None:  # noqa: D102
        # Check supported languages
        for fixture in self.__get_test_fixtures():
            with open(fixture[1], 'r') as i_fh:
                soup = BeautifulSoup(i_fh, 'html.parser')
            _, lang_key = main.guess_language(soup, SUPPORTED_LANGUAGES)
            assert lang_key == fixture[0]

        # Catch unsupported languages
        test_file = path.join(path.dirname(__file__), 'res', 'not-supported-lang.html')
        with open(test_file, 'r') as i_fh:
            soup = BeautifulSoup(i_fh, 'html.parser')
        with raises(ValueError):
            main.guess_language(soup, SUPPORTED_LANGUAGES)

    def __get_test_fixtures(self) -> Generator[Tuple[str, str], None, None]:
        res_path = path.join(path.dirname(__file__), 'res')
        for f in listdir():
            if not f.startswith('template-book-'):
                continue
            yield f[14:16], path.join(res_path, f)
