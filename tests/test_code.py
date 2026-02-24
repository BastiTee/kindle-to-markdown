"""Basic test suite."""

from os import listdir, path
from typing import Any

from bs4 import BeautifulSoup
from pytest import raises

from kindle_to_markdown import __main__ as main
from kindle_to_markdown.__main__ import NoteHeading
from kindle_to_markdown.languages import SUPPORTED_LANGUAGES


class TestCode:
    def test_extract_note_heading(self) -> None:
        for test_case in self.__get_extraction_test_fixtures():
            results = main.extract_note_heading(test_case[0], SUPPORTED_LANGUAGES['de'])
            assert test_case[1] == results

    def test_extract_language_keys_from_note_heading(self) -> None:
        for test_case in self.__get_extraction_test_fixtures():
            results = main.extract_language_keys_from_note_heading(test_case[0])
            assert test_case[2] == results

    def test_extract_annotations(self) -> None:
        for fixture in self.__get_language_test_fixtures():
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

    def test_guess_language(self) -> None:
        # Check supported languages
        for fixture in self.__get_language_test_fixtures():
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

    def __get_language_test_fixtures(self) -> list[tuple[str, str]]:
        res_path = path.join(path.dirname(__file__), 'res')
        fixtures = []
        for f in listdir(res_path):
            if not f.startswith('template-book-'):
                continue
            fixtures.append((f[14:16], path.join(res_path, f)))
        return fixtures

    def __get_extraction_test_fixtures(self) -> list[Any]:
        return [
            (
                'Markierung(gelb) - Seite 61 · Position 596',
                NoteHeading('textmark', '61', '596', None),
                ['Markierung', 'Seite', 'Position'],
            ),
            (
                'Markierung(gelb) - 8. Frag – aber > Seite 184 · Position 2304',
                NoteHeading('textmark', '184', '2304', '8. Frag - aber'),
                ['Markierung', 'Seite', 'Position'],
            ),
            (
                'Markierung(gelb) - Seite 99 · Position 652',
                NoteHeading('textmark', '99', '652', None),
                ['Markierung', 'Seite', 'Position'],
            ),
            (
                'Markierung(gelb) - Seite 28 · Position 407',
                NoteHeading('textmark', '28', '407', None),
                ['Markierung', 'Seite', 'Position'],
            ),
            (
                'Markierung(gelb) - Seite 229 · Position 3061',
                NoteHeading('textmark', '229', '3061', None),
                ['Markierung', 'Seite', 'Position'],
            ),
            (
                'Markierung(gelb) - RESISTANCE IS\n     INTERNAL > Position 148',
                NoteHeading('textmark', None, '148', 'RESISTANCE IS INTERNAL'),
                ['Markierung', 'Position'],
            ),
            (
                'Markierung(gelb) - Position 79',
                NoteHeading('textmark', None, '79', None),
                ['Markierung', 'Position'],
            ),
            (
                'Notiz - 5: Obsess Over Quality > Seite 175 · Position 2127',
                NoteHeading('note', '175', '2127', '5: Obsess Over Quality'),
                ['Notiz', 'Seite', 'Position'],
            ),
            (
                'Markierung(gelb) - Seite xi · Position 68',
                NoteHeading('textmark', 'xi', '68', None),
                ['Markierung', 'Seite', 'Position'],
            ),
            (
                'Markierung(gelb) - Chapter 1: The Matching Principle: How to Fail at Recruiting Spies > Seite 8 · Position 268',
                NoteHeading(
                    'textmark',
                    '8',
                    '268',
                    'Chapter 1: The Matching Principle: How to Fail at Recruiting Spies',
                ),
                ['Markierung', 'Seite', 'Position'],
            ),
        ]
