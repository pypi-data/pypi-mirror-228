# AxDumper

a simple json dumpers


## Usage

```python
    import json
    from axdumper import some_cool_dumper

    realy_not_dumpable_obj = RealyNotDumpableObj()

    json.dumps(
        realy_not_dumpable_obj, 
        default=event_json_dumper, 
        ensure_ascii=False, 
        indent=4
    )
    
    # And whoala! 🪄 
```

