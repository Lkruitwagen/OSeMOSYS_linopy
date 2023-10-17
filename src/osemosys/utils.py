import functools
import importlib
import io
import json
import os
import re
from datetime import datetime, timedelta  # noqa
from typing import Dict, Optional, List

import pandas as pd
from collections import defaultdict
import orjson

from osemosys.simpleeval import EvalWithCompoundTypes

def _indirect_cls(path):
    mod_name, _cls_name = path.rsplit(".", 1)
    mod = importlib.import_module(mod_name)
    _cls = getattr(mod, _cls_name)
    return _cls


def rsetattr(obj, attrs, val):
    pre = attrs[0:-1]
    post = attrs[-1]
    (rgetattr(obj, pre) if pre else obj)[post] = val
    return None


def rgetattr(obj, attrs, *args):
    def _getattr(obj, attr):
        return obj.get(attr)

    return functools.reduce(_getattr, [obj] + attrs)


def recursive_keys(keys, dictionary):
    for key, value in dictionary.items():
        if isinstance(value, dict):
            yield from recursive_keys(keys + [key], value)
        else:
            yield keys + [key]


def maybe_parse_environ(v):
    if isinstance(v, str):
        if "ENVIRON" in v:
            g = re.search(r"\(.*\)", v)
            return os.environ.get(v[g.start() + 1 : g.end() - 1], None)  # noqa
        else:
            return v
    else:
        return v

def maybe_subsitute_variables(txt, cfg):
    # TODO: Substitute {{$key.subkey}} here
    pass

def maybe_eval_string(expr):
    # TODO: check if we actually want to eval expression?

    evaluator = EvalWithCompoundTypes(functions={'sum':sum, 'range':range, 'max':max, 'min':min})

    return evaluator.eval(expr)


def walk_dict(d, f, *args):
    list_of_keys = recursive_keys([], d)

    for sublist in list_of_keys:
        val = rgetattr(d, sublist)
        rsetattr(d, sublist, f(val, *args))

    return d


def makehash():
    return defaultdict(makehash)


def _fill_d(d, target_column, data_columns, t):
    try:
        if len(data_columns) == 2:
            d[getattr(t, data_columns[0])][getattr(t, data_columns[1])] = getattr(
                t, target_column
            )
        elif len(data_columns) == 3:
            d[getattr(t, data_columns[0])][getattr(t, data_columns[1])][
                getattr(t, data_columns[2])
            ] = getattr(t, target_column)
        elif len(data_columns) == 4:
            d[getattr(t, data_columns[0])][getattr(t, data_columns[1])][
                getattr(t, data_columns[2])
            ][getattr(t, data_columns[3])] = getattr(t, target_column)
        else:
            raise NotImplementedError
    except Exception as e:
        print(t)
        print(target_column)
        print(data_columns)
        raise e

    return d


def group_to_json(
    g: pd.DataFrame,
    root_column: str,
    target_column: str = "value",
    data_columns: Optional[List[str]] = None,
    default_nodes: List[str] = None,
    fill_zero: bool = True,
):
    # non-mutable default
    if data_columns is None:
        data_columns = ["node_id", "commodity", "technology"]

    if default_nodes is not None:
        d = {n: makehash() for n in default_nodes}
    else:
        d = makehash()

    if not fill_zero:
        for t in g.drop(columns=[root_column]).loc[g[target_column] != 0].itertuples():
            _fill_d(d, target_column, data_columns, t)
    else:
        for t in g.drop(columns=[root_column]).itertuples():
            _fill_d(d, target_column, data_columns, t)

    return orjson.loads(orjson.dumps(d))