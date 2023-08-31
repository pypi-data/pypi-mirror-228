# -*- coding: utf-8 -*-
import locale
import os
import sys

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from codeboxcli.models.models import Base
from codeboxcli.models.models import Snippet
from codeboxcli.utils import default_editor
from codeboxcli.utils import messages
from codeboxcli.utils import pastebin

# Create a database engine
engine = create_engine(
    f'sqlite:///{os.path.expanduser("~/.codebox/database.db")}')

# Create tables based on models
Base.metadata.create_all(engine)

# Create a session factory
Session = sessionmaker(bind=engine)

# Extract the language code part
language_code = locale.getlocale()
if language_code:
    language_code = language_code[0].split('_')[0]


def share(args):
    global language_code

    if len(args) == 0:
        # Display help message and exit
        print(messages.help_share(language_code))
        return

    # Initialize default values for options
    expire_date = "1W"
    dev_key = os.getenv("CODEBOX_DEV_KEY")

    # Initialize loop index
    i = 0
    while i < len(args):
        if args[i] == "--help":
            # Display help message and exit
            print(messages.help_share(language_code))
            return
        elif args[i] == "--expire-date":
            # Handle expiration date option
            if i + 1 < len(args):
                expire_date = args[i + 1]
                i += 2
            else:
                print(messages.error_missing_value(
                    "--expire-date", language_code))
                return
        elif args[i] == "--dev-key":
            # Handle dev key option
            i += 1
            if i < len(args):
                dev_key = args[i]
                i += 1
            else:
                print(messages.error_missing_value("--dev-key", language_code))
                return
        else:
            i += 1

    # Check if there are enough arguments to proceed
    if len(args) < 1:
        print(messages.error_missing_argument("ID", language_code))
        return

    # Update a Snippet instance
    with Session() as session:
        snippet = session.query(Snippet).get(args[0])

        if snippet:
            pastebin.post(snippet.name, snippet.content, expire_date, dev_key)
        else:
            print(messages.error_not_found(args[0], language_code))
