# -*- coding: utf-8 -*-
"""Module main-file."""

from collections import namedtuple
from re import sub
from typing import Any, List, Optional, Tuple

import click
from bs4 import BeautifulSoup, PageElement

from kindle_to_markdown.languages import SUPPORTED_LANGUAGES

NoteHeading = namedtuple('NoteHeading', ['type', 'page', 'pos', 'chapter'])


def extract_note_heading(el_text: str, trsl: dict) -> NoteHeading:  # noqa: D103
    heading = __clean_text(el_text)

    # Extract the type
    type_: Optional[str] = None
    for key in trsl.keys():
        if heading.startswith(trsl[key]):
            type_ = key
    if not type_:
        raise ValueError(f'Unknown note heading type: {heading}')

    heading = sub(r'^[^-]+ - ', '', heading)
    chapter = None
    if ' > ' in heading:
        # Remove chapter name (we get this elsewhere)
        chapter = sub(r' > .*', '', heading)
        heading = sub(r'.* > ', '', heading)
    if ' · ' in heading:
        page = heading.split(' · ')[0].split(' ')[1]
        pos = heading.split(' · ')[1].split(' ')[1]
        return NoteHeading(type_, page, pos, chapter)
    else:
        pos = heading.split(' ')[1]
        return NoteHeading(type_, None, pos, chapter)


def __clean_text(el_text: str) -> str:
    for patt_rep in [
        (r'[“”«»]+', '"'),
        (r'[´`’\'‘‹›]+', '\''),
        (r'\.\.\.', '…'),
        (r'–', '-'),
        (r'[\n\t\s]+', ' '),
    ]:
        el_text = sub(patt_rep[0], patt_rep[1], el_text)
    return el_text


def extract_annotations(soup: BeautifulSoup, trsl: Any) -> List[str]:  # noqa: D103
    output: List[str] = []

    # Find title and author
    book_title = soup.find_all('div', class_='bookTitle')[0].text.strip()
    book_author = soup.find_all('div', class_='authors')[0].text.strip()
    output.append(f'# {book_author} - {book_title}\n')

    # Find all relevant elements
    elements: List[PageElement] = [
        p
        for p in soup.find_all(
            'div', class_=['noteHeading', 'noteText', 'sectionHeading']
        )
    ]
    note_head: NoteHeading
    curr_chapter: Optional[str] = None
    for el in elements:
        clazz = el['class'][0]
        if clazz == 'sectionHeading':
            heading = __clean_text(el.text.strip())
            output.append(f'## {heading}\n')
        elif clazz == 'noteHeading':
            # Assuming there is always a noteHeading before noteText
            note_head = extract_note_heading(el.text.strip(), trsl)

            # Format for output
            if note_head.page and note_head.pos:
                note_heading = f'p. {note_head.page}, pos. {note_head.pos}'
            else:
                note_heading = f'pos. {note_head.pos}'

            # Identify if new chapter and add if necessary
            if note_head.chapter and (
                note_head.chapter != curr_chapter or not curr_chapter
            ):
                output.append(f'### {note_head.chapter}\n')
                curr_chapter = note_head.chapter

            # Bookmarks have no further content
            if note_head.type == 'bookmark':
                output.append(f'> 🔖 {note_heading}\n')

        elif clazz == 'noteText':
            note_text = __clean_text(el.text.strip())
            if not note_text:  # Skip empty notes
                continue

            # Append content depending on type
            if note_head.type == 'textmark':
                output.append(f'{note_text} ({note_heading})\n')
            elif note_head.type == 'note':
                output.append(f'> {note_text} ({note_heading})\n')

    return output


def extract_language_keys_from_note_heading(el_text: str) -> List[str]:  # noqa: D103
    language_keys = []
    heading = __clean_text(el_text)
    h_split = heading.split(' - ', maxsplit=1)
    language_keys.append(h_split[0])
    if ' > ' in h_split[1]:  # Remove chapter name
        h_split[1] = sub(r'.* > ', '', h_split[1])
    if ' · ' in h_split[1]:
        language_keys += h_split[1].split(' · ', maxsplit=1)
    else:
        language_keys.append(h_split[1])
    language_keys = [sub(r'[\( ].*', '', lk) for lk in language_keys]
    return language_keys


def guess_language(  # noqa: D103
    soup: BeautifulSoup, languages: dict
) -> Tuple[dict[Any, Any], str]:
    # Extract the indicators of all the noteHeading elements
    note_headings = []
    for el in soup.find_all('div', class_='noteHeading'):
        note_headings += extract_language_keys_from_note_heading(el.text.strip())
    # These headings must be contained in the dictionary of a support language
    note_headings = list(set(note_headings))
    for lang_key in SUPPORTED_LANGUAGES.keys():
        if all([trsl in languages[lang_key].values() for trsl in note_headings]):
            return languages[lang_key], lang_key

    raise ValueError('Could not determine language. Is is probably not supported yet.')


def __check_if_output_file_is_needed(ctx: click.Context, param: Any, value: Any) -> Any:
    if not value:
        if ctx.params.get('print_only', False):
            return None
        raise click.BadParameter(
            'Option required unless \'--print-only\' / \'-p\' is set.'
        )
    return value


@click.command(
    help='A simple program to convert Kindle HTML annotations to a Markdown file.'
)
@click.option(
    '--input-file',
    '-i',
    required=True,
    type=click.Path(exists=True),
    help='Path to the Kindle annotations HTML file.',
)
@click.option(
    '--output-file',
    '-o',
    type=click.Path(),
    callback=__check_if_output_file_is_needed,
    help='Path to the Markdown file.',
)
@click.option(
    '--print-only', '-p', is_flag=True, help='Only print Markdown to the console.'
)
def main(input_file: str, output_file: str, print_only: bool) -> None:  # noqa: D103
    with open(input_file, 'r') as i_fh:
        soup = BeautifulSoup(i_fh, 'html.parser')

    try:
        trsl, _ = guess_language(soup, SUPPORTED_LANGUAGES)
    except ValueError as e:
        print(e)
        exit(1)

    output = extract_annotations(soup, trsl)

    for line in output:
        print(line)

    if not print_only:
        with open(output_file, 'w+') as o_fh:
            for line in output:
                o_fh.write(f'{line}\n')


if __name__ == '__main__':
    main()
