
import math
import numpy as np


def to_jsonable(obj):
    """Recursively convert numpy/scipy objects to JSON-safe Python primitives."""
    if isinstance(obj, np.ndarray):
        return [to_jsonable(x) for x in obj.tolist()]
    if isinstance(obj, np.generic):
        return to_jsonable(obj.item())
    if isinstance(obj, float):
        return obj if math.isfinite(obj) else None
    if isinstance(obj, (int, str, bool)) or obj is None:
        return obj
    if isinstance(obj, dict):
        return {str(to_jsonable(k)): to_jsonable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple, set)):
        return [to_jsonable(x) for x in obj]
    return str(obj)


def clamp(v, lo, hi):
    return max(lo, min(hi, v))


def pget(params, key, default):
    try:
        return float(params.get(key, default))
    except Exception:
        return default


def metric(label, value, unit='', status='neutral'):
    return {'label': label, 'value': round(float(value), 3), 'unit': unit, 'status': status}


def risk_level(score):
    if score >= 0.7:
        return 'high'
    if score >= 0.4:
        return 'medium'
    return 'low'


def safe_label(x):
    x = to_jsonable(x)
    return x if isinstance(x, str) else str(x)


def make_series(labels, values, name='Giá trị'):
    return {
        'labels': [safe_label(x) for x in labels],
        'series': [{'name': name, 'data': [round(float(x), 3) for x in values]}],
    }


def make_compare(labels, series):
    return {
        'labels': [safe_label(x) for x in labels],
        'series': [
            {'name': str(k), 'data': [round(float(x), 3) for x in v]}
            for k, v in series.items()
        ],
    }
