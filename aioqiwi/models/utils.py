from typing import List, Union

from .exceptions import ModelConversionError


def to_snake_case(s: str):
    """
    Returns snake_cased `s`
    """
    out = ""
    for n, sym in enumerate(s):
        if sym.isupper() and n > 0:
            out += "_" + sym
        else:
            out += sym
    return out.lower()


def to_upper_camel_case(s: str):
    """
    Returns CamelCased `s`
    """
    out = s
    for n, _ in enumerate(s):
        if s[n] in "-_":
            out = out.replace(s[n: n + 2], s[n + 1].upper(), 1)
    return out[0].upper() + out[1:]


def to_lower_camel_case(s: str):
    """
    Returns lowerCamelCased `s`
    """
    s = to_upper_camel_case(s)
    return s[0].lower() + s[1:]


def _raw_base_json_to_model(data: dict, model):
    """
    Raw conversion with control flow
    """
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


def hasattribute(model, attribute, val) -> bool:
    """
    Check if attribute exists in class checking from a raw qiwi update
    :param model: raw not initialized model
    :param attribute: model attribute
    :param val: value of attribute
    :return: boolean
    """

    if isinstance(val, dict):
        # if getattr(model, "_field_free_aioqiwi_model"):
        #     return True

        return hasattr(model, to_upper_camel_case(attribute))

    return to_snake_case(attribute) in vars(model)["__annotations__"]


def json_to_model(data: dict, model_type, model_to_list=None):
    """
    Converts json-type(dict) to model
    """
    model = model_type()
    data = {to_snake_case(k): v for k, v in data.items()}
    for key, val in data.items():
        if hasattribute(model_type, key, val):
            if isinstance(val, dict):
                new_model = getattr(model, to_upper_camel_case(key))
                setattr(model, to_upper_camel_case(key), json_to_model(val, new_model))

            elif isinstance(val, list):
                setattr(
                    model,
                    to_snake_case(key),
                    [
                        _raw_base_json_to_model(init_val, model_to_list)
                        for init_val in val
                    ],
                )

            else:
                setattr(model, to_snake_case(key), val)
        else:
            raise ModelConversionError(model_type, data)

    return model


def ignore_specs_get_list_of_models(data: Union[list, dict], model) -> List[type("model")]:
    """
    Converts json-array/json to models in list
    """
    items = []

    if isinstance(data, list):
        for val in data:
            items.append(json_to_model(val, model))

    elif isinstance(data, dict):
        for val in data.values():
            if isinstance(val, list):
                for init_dict in val:
                    items.append(json_to_model(init_dict, model))

    else:
        raise ValueError(f"Expected type list or dict, got {type(data)}")

    return items
