from datetime import datetime
from axdumper.types import DictConvertAble, StringifyAble


def telethon_event_json_dumper(obj):
    if isinstance(obj, DictConvertAble):
        return obj.to_dict()
    if isinstance(obj, StringifyAble):
        return obj.stringify()
    if isinstance(obj, datetime):
        return obj.strftime("%d-%m-%Y, %H:%M:%S")
    return repr(obj)

