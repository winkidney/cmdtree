import sys


WIN = sys.platform.startswith('win')


def get_filesystem_encoding():
    return sys.getfilesystemencoding() or sys.getdefaultencoding()

if WIN:
    def _get_argv_encoding():
        import locale
        return locale.getpreferredencoding()
else:
    def _get_argv_encoding():
        return getattr(sys.stdin, 'encoding', None) or get_filesystem_encoding()