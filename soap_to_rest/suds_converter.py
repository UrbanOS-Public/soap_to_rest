from itertools import starmap
from suds.sudsobject import asdict as suds_as_dict

def suds_to_dict(value):
  if _is_primordial(value):
    return _list_wrap(value)
  if not _is_suds_object(value):
    return value
  if _is_array(value):
    array = _get_array_from_suds_object(value)
    return list(map(convert_value, array))
  else:
    key_value_entries = suds_as_dict(value).items()
    converted = list(starmap(convert_entry, key_value_entries))
    return dict(converted)

def _is_primordial(value):
  return not hasattr(value, '__dict__')

def _is_suds_object(value):
  return hasattr(value, '__keylist__')

def _list_wrap(value):
  if _is_list(value):
    return value

  return [value]

def _is_list(value):
  return isinstance(value, (list, tuple))

def _get_class_name(sudso):
  return sudso.__class__.__name__


def _get_array_from_suds_object(sudso):
  return sudso[sudso.__keylist__[0]]


def _is_array(object):
  obj_suds_as_dict = suds_as_dict(object)
  if len(obj_suds_as_dict) == 1:
    possible_array = list(obj_suds_as_dict.values())[0]

    return isinstance(possible_array, (list, tuple))
  
  return False


def convert_entry(k, v):
  if hasattr(v, '__keylist__'):
    return (k, suds_to_dict(v))
  elif isinstance(v, list):
    return (k, list(map(convert_value, v)))
  else:
    return (k, v)

    
def convert_value(v):
  if hasattr(v, '__keylist__'):
      return suds_to_dict(v)
  else:
      return v