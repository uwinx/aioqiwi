def to_dict(cls):
    out_dict = {}

    for key, val in cls.__dict__.items():
        if key[0] != "_":
            if issubclass(type(key), BaseModel):
                out_dict[key] = val.as_dict()
            else:
                out_dict[key] = val

    return out_dict


class BaseModel:
    @property
    def dict_params(self) -> dict:
        """
        Get Mapping of public attributes of inherited class
        :return: dict
        """
        return to_dict(self)
