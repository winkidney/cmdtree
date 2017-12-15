import sys


def error(error_msg):
    sys.stderr.write(error_msg)
    sys.stderr.write("\n")


def format_list(the_list):
    return "\n".join(str(ele) for ele in the_list)