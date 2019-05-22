from typing import List


def to_snake_case(s: str):
    out = ""
    for n, sym in enumerate(s):
        if sym.isupper() and n > 0:
            out += "_" + sym
        else:
            out += sym
    return out.lower()


def to_upper_camel_case(s: str):
    out = s
    for n, letter in enumerate(s):
        if s[n] in "-_":
            out = out.replace(s[n : n + 2], s[n + 1].upper(), 1)
    return out[0].upper() + out[1:]


def to_lower_camel_case(s: str):
    s = to_upper_camel_case(s)
    return s[0].lower() + s[1:]


def _raw_base_json_to_model(data: dict, model):
    model = model()

    for key, val in data.items():
        if isinstance(val, dict):
            init_class = getattr(model, to_upper_camel_case(key))()
            for ikey, ival in val.items():
                if not isinstance(ival, dict):
                    setattr(init_class, to_snake_case(ikey), ival)
            setattr(model, to_upper_camel_case(key), init_class)
        else:
            setattr(model, to_snake_case(key), val)

    return model


def json_to_model(data: dict, model_type, model_to_list=None):
    model = model_type()

    for key, val in data.items():
        if isinstance(val, dict):
            new_model = getattr(model, to_upper_camel_case(key))
            setattr(model, to_upper_camel_case(key), json_to_model(val, new_model))

        elif isinstance(val, list):
            setattr(
                model,
                to_snake_case(key),
                [_raw_base_json_to_model(init_val, model_to_list) for init_val in val],
            )

        else:
            setattr(model, to_snake_case(key), val)

    return model


def ignore_specs_get_list_of_models(data: dict, model) -> List[type("model")]:
    items = []

    for key, val in data.items():
        if isinstance(val, list):
            for init_dict in val:
                items.append(json_to_model(init_dict, model))

    return items
