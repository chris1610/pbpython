""" Generate responsive HTML emails from Markdown files used in a pelican blog.

Refer to https://pbpython.com/ for the details.

"""
from markdown2 import Markdown
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from premailer import transform
from argparse import ArgumentParser
from bs4 import BeautifulSoup


def parse_args():
    """Parse the command line input
    
    Returns:
        args -- ArgumentParser object
    """
    parser = ArgumentParser(
        description='Generate HTML email from markdown file')
    parser.add_argument('doc', action='store', help='Markdown input document')

    parser.add_argument('-t',
                        help='email HTML template',
                        default='template.html')
    parser.add_argument(
        '-o', help='output filename. Default is inputfile_email.html')
    args = parser.parse_args()
    return args


def create_HTML(config):
    """Read in the source markdown file and convert it to a standalone
    HTML file suitable for emailing

    Arguments:
        config -- ArgumentParser object that contains the input file
    """
    # Define all the file locations
    in_doc = Path(config.doc)
    if config.o:
        out_file = Path(config.o)
    else:
        out_file = Path.cwd() / f'{in_doc.stem}_email.html'
    template_file = config.t

    # Read in the entire file as a list
    # This can be problematic if the file is really large
    with open(in_doc) as f:
        all_content = f.readlines()

    # Get the title line and clean it up
    title_line = all_content[0]
    title = f'My Newsletter - {title_line[7:].strip()}'

    # Parse out the body from the meta data content at the top of the file
    body_content = all_content[6:]

    # Create a markdown object and convert the list of file lines to HTML
    markdowner = Markdown()
    markdown_content = markdowner.convert(''.join(body_content))

    # Set up jinja templates
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template(template_file)

    # Define the template variables and render
    template_vars = {'email_content': markdown_content, 'title': title}
    raw_html = template.render(template_vars)

    # Generate the final output string
    # Inline all the CSS using premailer.transform
    # Use BeautifulSoup to make the formatting nicer
    soup = BeautifulSoup(transform(raw_html),
                         'html.parser').prettify(formatter="html")

    # The unsubscribe tag gets mangled. Clean it up.
    final_HTML = str(soup).replace('%7B%7BUnsubscribeURL%7D%7D',
                                   '{{UnsubscribeURL}}')
    out_file.write_text(final_HTML)


if __name__ == '__main__':
    conf = parse_args()
    print('Creating output HTML')
    create_HTML(conf)
    print('Completed')
