#!/usr/bin/env python
# coding: utf-8
import os
import shutil

import click
import nbformat as nbformat

from exporters import jupyter, slides

HTML_RENDERER_REL_PATH = 'html_renderer'
HTML_RENDERER_ABS_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), HTML_RENDERER_REL_PATH)
HTML_SLIDES_TEMPLATE_FILE_NAME = os.path.join(HTML_RENDERER_ABS_PATH, 'template.html')


class MD2JupyterError(Exception):
    pass


@click.command()
@click.argument('source_md_file', type=click.File('r'))
@click.argument('destination_directory', type=click.Path(resolve_path=True, file_okay=False), required=False)
@click.option('--format', default='both', type=click.Choice(['html', 'ipynb', 'both']), help='Desired format')
@click.option('--force_overwrite', '-f', is_flag=True, default=False, help='Overwrite destination directory')
def convert(source_md_file, destination_directory, format, force_overwrite):
    slides_md = source_md_file.read()

    if not destination_directory:
        source_md_file_name = os.path.basename(source_md_file.name)
        destination_directory = os.path.splitext(source_md_file_name)[0]

    if os.path.exists(destination_directory) and force_overwrite:
        shutil.rmtree(destination_directory)
    try:
        shutil.copytree(
            os.path.abspath(os.path.dirname(source_md_file.name)),
            destination_directory,
            ignore=shutil.ignore_patterns(destination_directory, source_md_file.name)
        )
    except FileExistsError:
        raise MD2JupyterError('Destination directory is already exists. Use `-f` flag to completely rewrite it.')

    if format in ('both', 'html'):
        try:
            shutil.copytree(HTML_RENDERER_ABS_PATH, os.path.join(destination_directory, HTML_RENDERER_REL_PATH))
        except FileExistsError:
            # Seems that ve'we copied html_renderer previously
            pass

        slides_template_html = open(HTML_SLIDES_TEMPLATE_FILE_NAME).read()
        slides_html = slides_template_html.format(slides.exporter.render(slides_md))
        open(os.path.join(destination_directory, 'slides.html'), 'w').write(slides_html)

    if format in ('both', 'ipynb'):
        jypyter_notebook = jupyter.exporter.render(slides_md)
        nbformat.write(jypyter_notebook, os.path.join(destination_directory, 'slides.ipynb'))

if __name__ == '__main__':
    convert()
