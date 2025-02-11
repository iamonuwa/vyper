import types

from vyper.settings import (
    VYPER_ERROR_CONTEXT_LINES,
    VYPER_ERROR_LINE_NUMBERS,
)


# Attempts to display the line and column of violating code.
class ParserException(Exception):
    def __init__(self, message='Error Message not found.', item=None):
        self.message = message
        self.lineno = None
        self.col_offset = None

        if isinstance(item, tuple):  # is a position.
            self.lineno, self.col_offset = item[:2]
        elif item and hasattr(item, 'lineno'):
            self.set_err_pos(item.lineno, item.col_offset)
            if hasattr(item, 'source_code'):
                self.source_code = item.source_code

    def set_err_pos(self, lineno, col_offset):
        if not self.lineno:
            self.lineno = lineno

            if not self.col_offset:
                self.col_offset = col_offset

    def __str__(self):
        lineno, col_offset = self.lineno, self.col_offset

        if lineno is not None and hasattr(self, 'source_code'):
            from vyper.utils import annotate_source_code

            source_annotation = annotate_source_code(
                self.source_code,
                lineno,
                col_offset,
                context_lines=VYPER_ERROR_CONTEXT_LINES,
                line_numbers=VYPER_ERROR_LINE_NUMBERS,
            )
            col_offset_str = '' if col_offset is None else str(col_offset)
            return f'line {lineno}:{col_offset_str} {self.message}\n{source_annotation}'

        elif lineno is not None and col_offset is not None:
            return f'line {lineno}:{col_offset} {self.message}'

        return self.message


class PythonSyntaxException(ParserException):
    """
    Conversion from error using ast.parse()
    """
    def __init__(self, syntax_error: SyntaxError, source_code: str):
        item = types.SimpleNamespace()  # TODO: Create an actual object for this
        item.lineno = syntax_error.lineno
        item.col_offset = syntax_error.offset
        item.source_code = source_code
        super().__init__(message=f'SyntaxError: {syntax_error.msg}', item=item)


class VariableDeclarationException(ParserException):
    """ Throws invalid variable declaration exception """
    pass


class StructureException(ParserException):
    """ Throws invalid structure exception """
    pass


class ConstancyViolationException(ParserException):
    """ Throws exception when constant assumptions are violated during compile-time or run-time """
    pass


class NonPayableViolationException(ParserException):
    pass


class InvalidLiteralException(ParserException):
    pass


class InvalidTypeException(ParserException):
    pass


class TypeMismatchException(ParserException):
    pass


class FunctionDeclarationException(ParserException):
    pass


class EventDeclarationException(ParserException):
    pass


class VersionException(ParserException):
    """Throws version exception"""
    pass


class SyntaxException(ParserException):
    """Throws Syntax exception"""
    pass


class ArrayIndexException(ParserException):
    """Throws Array index exception"""
    pass


class CompilerPanic(Exception):
    """
    Throw Compiler exception
    """

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message + ' Please create an issue.'


class JSONError(Exception):
    """
    Throws JSON error exception
    """

    def __init__(self, msg, lineno=None, col_offset=None):
        super().__init__(msg)
        self.lineno = lineno
        self.col_offset = col_offset
