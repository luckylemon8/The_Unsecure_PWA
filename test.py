import re


def check_password(password):
    if not re.search(r"[@$!%*?&]", password):
        raise ValueError("does not contain one of '@$!%*?&' special characters")


check_password("fgid")
