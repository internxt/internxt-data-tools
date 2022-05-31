import collections
import json
import collections
import sys

if sys.version_info.major == 3 and sys.version_info.minor >= 10:
    from collections.abc import MutableMapping
else:
    from collections import MutableMapping


def flatten(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def flatten_extract(schema, obj):
  obj = flatten(obj)
  minimum_schema = filter(lambda key: key in obj.keys(), schema)
  return {key: obj[key] for key in minimum_schema}


def extract_schema_data(schema, list):
  return [flatten_extract(schema, item)for item in list]


def flatten_items_list(element_list):
  return [flatten(item) for item in element_list]

# Needs Refactor


def remove_lists(d, key='data'):
  if(not isinstance(d, dict)):
    return d
  new = {}
  for k, v in d.items():
    aux = v
    if isinstance(v, dict):
      aux = remove_lists(v, key)
    if isinstance(v, list) and len(v) > 0:
      aux = v[0]
      aux = remove_lists(aux, key)
    new[k] = aux
  return new


def bulk_remove_lists(l):
  return [remove_lists(json.loads(str(item))) for item in l]
