from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    LONG_DESCRIPTION = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'Sending Mails Made Easy'


# Setting up
setup(
    name="Qmail",
    version=VERSION,
    author="Akmal Riyas",
    author_email="akmalriyas@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages= ["Qmail"],
   
    keywords=['python', 'mail', 'email', 'easymail','gmail','send_mail', 'otp', 'passwordgen'],
    dependency_links=[
        'https://github.com/Akmal-Riyas/Qmail/tree/mains'
    ],

)