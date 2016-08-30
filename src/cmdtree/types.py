from argparse import ArgumentTypeError as ArgTypeError, FileType

from six import text_type, PY2

from ._compat import _get_argv_encoding, get_filesystem_encoding


class ParamTypeFactory(object):
    """
    Helper class for type convention.
    """

    name = None

    def __call__(self):
        """
        Return keyword arguments for add_argument function.
        :rtype: dict
        """
        return {"type": self.convert}

    def convert(self, value):
        raise NotImplementedError(
            "type converter should be implemented before used"
            "for value {value}".format(value=value)
        )

    @staticmethod
    def fail(msg):
        raise ArgTypeError(msg)


class UnprocessedParamType(ParamTypeFactory):
    name = 'text'

    def convert(self, value):
        return value

    def __repr__(self):
        return 'UNPROCESSED'


class StringParamType(ParamTypeFactory):
    name = 'text'

    def convert(self, value):
        if isinstance(value, bytes):
            enc = _get_argv_encoding()
            try:
                value = value.decode(enc)
            except UnicodeError:
                fs_enc = get_filesystem_encoding()
                if fs_enc != enc:
                    try:
                        value = value.decode(fs_enc)
                    except UnicodeError:
                        value = value.decode('utf-8', 'replace')
            return value
        return value

    def __repr__(self):
        return 'STRING'


class IntParamType(ParamTypeFactory):
    name = 'integer'

    def convert(self, value):
        try:
            return int(value)
        except (ValueError, UnicodeError):
            self.fail('%s is not a valid integer' % value)

    def __repr__(self):
        return 'INT'


class IntRange(IntParamType):
    name = 'integer range'

    def __init__(self, min=None, max=None, clamp=False):
        self.min = min
        self.max = max
        self.clamp = clamp

    def convert(self, value):
        rv = IntParamType.convert(self, value)
        if self.clamp:
            if self.min is not None and rv < self.min:
                return self.min
            if self.max is not None and rv > self.max:
                return self.max
        if self.min is not None and rv < self.min or \
           self.max is not None and rv > self.max:
            if self.min is None:
                self.fail('%s is bigger than the maximum valid value '
                          '%s.' % (rv, self.max))
            elif self.max is None:
                self.fail('%s is smaller than the minimum valid value '
                          '%s.' % (rv, self.min))
            else:
                self.fail('%s is not in the valid range of %s to %s.'
                          % (rv, self.min, self.max))
        return rv

    def __repr__(self):
        return 'IntRange(%r, %r)' % (self.min, self.max)


class BoolParamType(ParamTypeFactory):
    name = 'boolean'

    def convert(self, value):
        if isinstance(value, bool):
            return bool(value)
        value = value.lower()
        if value in ('true', '1', 'yes', 'y'):
            return True
        elif value in ('false', '0', 'no', 'n'):
            return False
        self.fail('%s is not a valid boolean' % value)

    def __repr__(self):
        return 'BOOL'


class FloatParamType(ParamTypeFactory):
    name = 'float'

    def convert(self, value):
        try:
            return float(value)
        except (UnicodeError, ValueError):
            self.fail(
                '%s is not a valid floating point value' % value
            )

    def __repr__(self):
        return 'FLOAT'


class UUIDParameterType(ParamTypeFactory):
    name = 'uuid'

    def convert(self, value):
        import uuid
        try:
            if PY2 and isinstance(value, text_type):
                value = value.encode('ascii')
            return uuid.UUID(value)
        except (UnicodeError, ValueError):
            self.fail('%s is not a valid UUID value' % value)

    def __repr__(self):
        return 'UUID'


class File(ParamTypeFactory):

    name = "filename"

    def __init__(self, mode="r", bufsize=-1):
        self.factory = FileType(mode=mode, bufsize=bufsize)

    def convert(self, value):
        return self.factory(value)


class Choices(UnprocessedParamType):

    def __init__(self, choices, type=None):
        """
        :type choices: tuple or list
        :type type: callable
        :param type: type convention function for all choices.
        Receives a `func(value)` as its argument.
        """
        assert hasattr(choices, "index")
        self.choices = choices or tuple()
        self.type = type

    def __call__(self):
        """
        Return keyword arguments
        :rtype: dict
        """
        return {
            "type": self.type or self.convert,
            "choices": self.choices
        }


UNPROCESSED = UnprocessedParamType()

STRING = StringParamType()

INT = IntParamType()

FLOAT = FloatParamType()

BOOL = BoolParamType()

UUID = UUIDParameterType()