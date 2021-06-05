def nested_key(obj:dict, keys:list, *, default=None, required=False):
    res = obj
    for key in keys:
        if key in res:
            res = res[key]
        else:
            if required:
                print(f"{'->'.join(keys)} is not defined and is required")
                exit(0)
                #raise NameError(f"{'->'.join(keys)} is not defined and is required")
            return default
    return res