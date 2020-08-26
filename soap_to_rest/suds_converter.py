"""
Converter that can take (usually) a suds object
and turn it into a serializable dict, array, etc.
"""
from itertools import starmap

from suds.sudsobject import asdict as suds_as_dict


def to_serializable(value):
    """
    Recursively convert a value returned by a suds client
    into a serializable format (array, object, primordial value, etc.)
    """
    if _is_primordial(value):
        return _list_wrap(value)

    return _convert_to_serializable(value)


def _convert_to_serializable(value):
    if _is_list(value):
        return _convert_values(value)

    if not _is_suds_object(value):
        return value

    suds_dict = suds_as_dict(value)

    if _is_suds_array(suds_dict):
        return _convert_suds_array(suds_dict)

    return _convert_suds_object(suds_dict)


def _convert_suds_array(suds_dict):
    array = _get_first_value_from_dict(suds_dict)
    return _convert_values(array)


def _convert_suds_object(dictionary):
    return _convert_entries(dictionary.items())


def _convert_entries(entries):
    return dict(list(starmap(_convert_entry, entries)))


def _convert_entry(key, value):
    return (key, _convert_to_serializable(value))


def _convert_values(values):
    return list(map(_convert_to_serializable, values))


def _is_primordial(value):
    return not hasattr(value, "__dict__")


def _is_suds_object(value):
    return hasattr(value, "__keylist__")


def _is_suds_array(suds_dict):
    if len(suds_dict) == 1:
        possible_array = _get_first_value_from_dict(suds_dict)

        return _is_list(possible_array)

    return False


def _list_wrap(value):
    if _is_list(value):
        return value

    return [value]


def _is_list(value):
    return isinstance(value, (list, tuple))


def _get_first_value_from_dict(suds_dict):
    return list(suds_dict.values())[0]
