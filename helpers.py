import re

def sanitize(val):
    return val.replace("\"", "\"\"")

# remove all special characters from name so it can be used as a file name
def make_name_safe(name):
    res = re.sub(r"[^ a-zA-Z0-9]+",'',name)
    res = res.replace(" ", "-")
    # TODO: what should we return if the resulting string is ""?
    return res
