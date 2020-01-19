# Markdown to HTML Email

This sample code accompanies the [article](https://pbpython.com/markdown-email.html) on Practical Business Python. Refer to the article for more background and details on the rationale
for the project.

## Getting started

This is a standalone script that will take a simple markdown file as input, 
convert the markdown to HTML and insert it in the template file.

Sample input files are included in order to illustrate the concept.
The two input files are sample_doc.md which contains the content and
template.html which contain the HTML structure that should render 
as a responsive email.

### Prerequisites
This script requires python >= 3.5 and the following dependencise:

* [python-markdown2](https://github.com/trentm/python-markdown2)
* [jinja](https://jinja.palletsprojects.com/en/2.10.x/)
* [premailer](https://github.com/peterbe/premailer)
* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

## Using the script
The script is run from the command line. 

To see the help:
```
python email_gen.py --help

usage: email_gen.py [-h] [-t T] [-o O] doc

Generate HTML email from markdown file

positional arguments:
  doc         Markdown input document

optional arguments:
  -h, --help  show this help message and exit
  -t T        email HTML template
  -o O        output filename. Default is inputfile_email.html

```

Using the sample template file on the provided file:

```
python email_gen.py sample_doc.md
```

Will generate a inlined HTML file titled sample_doc_email.html that can be copied
into an HTML email.

## License
This software is released under the BSD 3-Clause License.