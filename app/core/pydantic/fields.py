from pydantic import Schema, errors, ConstrainedStr
from pydantic.types import constr_strip_whitespace, constr_length_validator
from pydantic.validators import not_none_validator, str_validator


class ProjectStrictStr(ConstrainedStr):
    regex = None
    min_length = None
    max_length = None

    @classmethod
    def __get_validators__(cls):
        yield cls.validate
        yield not_none_validator
        yield constr_strip_whitespace
        yield constr_length_validator

    @classmethod
    def validate(cls, value):
        if not isinstance(value, str):
            raise errors.StrError()

        if cls.curtail_length and len(value) > cls.curtail_length:
            value = value[: cls.curtail_length]

        if cls.regex:
            print("here")
            if not cls.regex.match(value):
                raise errors.StrRegexError(pattern=cls.regex.pattern)

        return value
