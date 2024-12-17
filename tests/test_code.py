# -*- coding: utf-8 -*-
"""Basic test suite."""

import __future__  # noqa: F401

from os import path
from typing import Tuple

from bs4 import BeautifulSoup
from pytest import raises

from kindle_to_markdown import __main__ as main
from kindle_to_markdown.__main__ import LANG, NoteHeading


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
            results = main.extract_note_heading(test_case[0], LANG['de'])
            assert test_case[1] == results

    def test_language_en(self) -> None:  # noqa: D102
        # Load language
        assert 'en' in LANG.keys()
        trsl = LANG['en']

        # Read template file
        test_file = path.join(path.dirname(__file__), 'res', 'template-book-en.html')
        with open(test_file, 'r') as i_fh:
            soup = BeautifulSoup(i_fh, 'html.parser')

        output = main.extract_annotations(soup, trsl)
        assert output == [
            '# Basti Tee - My ebook\n',
            '## First Section\n',
            '> 🔖 p. 5, pos. 28\n',
            'A marked text. (p. 5, pos. 35)\n',
            'More marked text. (p. 6, pos. 44)\n',
            '> Personal note (p. 6, pos. 44)\n',
            '> Note without marking text. (p. 6, pos. 49)\n',
        ]

    def test_language_de(self) -> None:  # noqa: D102
        # Load language
        assert 'de' in LANG.keys()
        trsl = LANG['de']

        # Read template file
        test_file = path.join(path.dirname(__file__), 'res', 'template-book-de.html')
        with open(test_file, 'r') as i_fh:
            soup = BeautifulSoup(i_fh, 'html.parser')

        output = main.extract_annotations(soup, trsl)
        assert output == [
            '# Basti Tee - My ebook\n',
            '## Erster Abschnitt\n',
            '> 🔖 p. 5, pos. 28\n',
            'Ein markierter Text. (p. 5, pos. 35)\n',
            'Mehr markierter Text. (p. 6, pos. 44)\n',
            '> Persönliche Notiz. (p. 6, pos. 44)\n',
            '> Notiz ohne Text (p. 6, pos. 49)\n',
        ]

    def test_guess_language(self) -> None:  # noqa: D102
        # Identify supported languages
        for test_case in [
            ('de', 'template-book-de.html'),
            ('en', 'template-book-en.html'),
        ]:
            test_file = path.join(path.dirname(__file__), 'res', test_case[1])
            with open(test_file, 'r') as i_fh:
                soup = BeautifulSoup(i_fh, 'html.parser')
            _, lang_key = main.guess_language(soup, LANG)
            assert lang_key == test_case[0]

        # Catch unsupported languages
        test_file = path.join(
            path.dirname(__file__), 'res', 'template-book-not-supported-lang.html'
        )
        with open(test_file, 'r') as i_fh:
            soup = BeautifulSoup(i_fh, 'html.parser')
        with raises(ValueError):
            main.guess_language(soup, LANG)
