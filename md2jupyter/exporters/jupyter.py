# coding: utf-8
import re

import mistune
from nbformat.v4 import nbbase

from .common import SLIDE_REGEX


class JupyterGrammar(mistune.BlockGrammar):
    slide = SLIDE_REGEX

    # surrounded_patterns = [r'{}'.format(mistune._pure_pattern(lexer)) for lexer in (slide, mistune.BlockGrammar.block_code)]
    # exclude_from_as_is = r'|'.join(surrounded_patterns)

    as_is = re.compile(r'^(.+?)(?=!!!|```)', re.MULTILINE | re.DOTALL)
    rest_part = re.compile(r'(.*)', re.MULTILINE | re.DOTALL)


class JupyterLexer(mistune.BlockLexer):
    default_rules = ['slide', 'block_code', 'fences', 'as_is', 'rest_part']  # + mistune.BlockLexer.default_rules

    def parse_slide(self, pattern_match):
        self.tokens.append({'type': 'slide_begin'})
        self.parse(pattern_match.group('next_slide') or pattern_match.group('last_slide'))

    def parse_as_is(self, pattern_match):
        self.tokens.append({
            'type': 'as_is',
            'text': pattern_match.group(0),
        })

    def parse_rest_part(self, pattern_match):
        self.parse_as_is(pattern_match)


class JupyterRenderer(mistune.Renderer):
    def placeholder(self):
        return []

    def slide_begin(self):
        pass

    def slide_end(self):
        pass

    def block_code(self, code, lang=None):
        return nbbase.new_code_cell(source=code)

    def as_is(self, text):
        return nbbase.new_markdown_cell(source=text)

        # return '</section>'


class JupyterMarkdown(mistune.Markdown):
    def output(self, text, rules=None):
        self.tokens = self.block(text, rules)
        self.tokens.reverse()

        self.inline.setup(self.block.def_links, self.block.def_footnotes)

        out = self.renderer.placeholder()
        while self.pop():
            rendered = self.tok()
            if rendered:
                out.append(rendered)

        return nbbase.new_notebook(cells=out)

    def output_slide_begin(self):
        return self.renderer.slide_begin()

    def output_slide_end(self):
        return self.renderer.slide_end()

    def output_as_is(self):
        return self.renderer.as_is(self.token['text'])


exporter = JupyterMarkdown(JupyterRenderer(), block=JupyterLexer(JupyterGrammar()))
