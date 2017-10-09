# coding: utf-8
import mistune

from .common import SLIDE_REGEX


class MDSlidesGrammar(mistune.BlockGrammar):
    slide = SLIDE_REGEX


class MDSlidesBlockLexer(mistune.BlockLexer):
    default_rules = ['slide', ] + mistune.BlockLexer.default_rules

    def parse_slide(self, pattern_match):
        self.tokens.append({'type': 'slide_begin'})
        self.parse(pattern_match.group('next_slide') or pattern_match.group('last_slide'))
        self.tokens.append({'type': 'slide_end'})


class MDSlidesRenderer(mistune.Renderer):

    def slide_begin(self):
        return '<section class="slide">'

    def slide_end(self):
        return '</section>'


class MDSlidesMarkdown(mistune.Markdown):

    def output_slide_begin(self):
        return self.renderer.slide_begin()

    def output_slide_end(self):
        return self.renderer.slide_end()

exporter = MDSlidesMarkdown(MDSlidesRenderer(), block=MDSlidesBlockLexer(MDSlidesGrammar()))
