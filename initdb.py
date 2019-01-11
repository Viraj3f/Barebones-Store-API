"""
Creates the database file and adds some stub data.
"""

from barebones import db


if __name__ == "__main__":
    # Creates the database instance.
    db.create_all()
