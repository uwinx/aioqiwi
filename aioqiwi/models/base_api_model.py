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
    # special design
    # return whole class as_dict not only param.
    @classmethod
    def as_dict(cls):
        return to_dict(cls)

    @property
    def dict_params(self):
        # this shit is dirty hack
        return to_dict(self)
