import collections
import json


def coerce(vtype, value):
    if vtype == "i":
        return int(value)
    elif vtype == "d":
        return float(value)
    elif vtype == "s":
        return str(value)
    return None


def infer_types(values):
    vtype = type(values)
    if vtype is str:
        return "s"
    elif vtype is float:
        return "d"
    elif vtype is int:
        return "i"
    elif type(values) is list or type(values) is tuple:
        return [infer_types(v) for v in values]
    return None


class JSONDataPortal(collections.UserDict):
    """
    This class extends the dict class to unpack data that is
    represented in a compact form.
    """

    def __init__(self, packed_data, filename=None):
        collections.UserDict.__init__(self)
        self.data = packed_data
        self._filename=filename

    def is_set(self, name):
        return name in self.data and type(self.data[name]) is dict and 'set_type' in self.data[name]

    def is_parameter(self, name):
        return name in self.data and (type(self.data[name]) is not dict or 'set_type' not in self.data[name])

    def parameters(self):
        for name in self.data:
            if self.is_parameter(name):
                yield name

    def sets(self):
        for name in self.data:
            if self.is_set(name):
                yield name

    def _load_data(self):
        if self._filename:
            with open(self._filename, "r") as INPUT:
                self.data = json.load(INPUT)

    def __getitem__(self, name):
        self._load_data()
        assert name in self.data, f"Missing data '{name}'"
        return self._unpack(self.data[name])

    def __setitem__(self, name, data):
        self.data[name] = self._pack(data)


class JSONDataPortal_Coek(JSONDataPortal):
    """
    This class unpacks data using the Coek DataPortal schema.
    """

    def _unpack(self, data):
        if type(data) is dict:
            #
            # Dict data may be either sets, indexed sets or indexed parameters.
            #
            assert "data" in data, "Malformed data specification"
            if "key_type" in data:
                #
                # Indexed data
                #
                ktype = data["key_type"]
                if type(ktype) is list:
                    klen = len(ktype)
                else:
                    klen = 0

                if "set_type" in data:
                    #
                    # Indexed sets
                    #
                    stype = data["set_type"]
                    if type(stype) is list:
                        slen = len(stype)
                    else:
                        slen = 0

                    retval = {}
                    for val in data["data"]:
                        k, v = val
                        #
                        # Form key
                        #
                        if klen > 0:
                            key = tuple(coerce(ktype[i], k[i]) for i in range(klen))
                        else:
                            key = k
                        #
                        # Form value
                        #
                        if slen > 0:
                            value = [
                                tuple(coerce(stype[i], sval[i]) for i in range(slen))
                                for sval in v
                            ]
                        else:
                            value = [coerce(stype, sval) for sval in v]

                        retval[key] = value

                    return retval

                else:
                    #
                    # Indexed parameters
                    #
                    ptype = data["param_type"]
                    if type(ptype) is list:
                        plen = len(ptype)
                    else:
                        plen = 0

                    retval = {}
                    for val in data["data"]:
                        k, v = val
                        #
                        # Form key
                        #
                        if klen > 0:
                            key = tuple(coerce(ktype[i], k[i]) for i in range(klen))
                        else:
                            key = k
                        #
                        # Form value
                        #
                        if plen > 0:
                            value = tuple(coerce(ptype[i], v[i]) for i in range(plen))
                        else:
                            value = coerce(ptype, v)

                        retval[key] = value

                    return retval

            else:
                #
                # Set data
                #
                assert "set_type" in data, "Malformed data specification"
                stype = data["set_type"]
                if type(stype) is list:
                    slen = len(stype)
                else:
                    slen = 0
                if slen > 0:
                    return [
                        tuple(coerce(stype[i], sval[i]) for i in range(slen))
                        for sval in data["data"]
                    ]
                else:
                    return [coerce(stype, sval) for sval in data["data"]]

        elif type(data) is list:
            #
            # List data is assumed to be a tuple parameter.
            #
            return tuple(data)
        else:
            #
            # Simple data types are simple parameter values: integer, double or string.
            #
            return data

    def _pack(self, data):
        if type(data) is dict:
            setflag = None
            #
            # Indexed data
            #
            datavals = []
            for k, v in data.items():
                if type(k) is tuple:
                    key = list(k)
                else:
                    key = k

                if type(v) is list:
                    setflag=True
                    if type(v[0]) is tuple:
                        value = [list(value) for value in v]
                    else:
                        value = v
                elif type(v) is tuple:
                    setflag=False
                    value = list(v)
                else:
                    value = v

                datavals.append([key, value])

            if type(datavals[0][1]) is list:
                assert setflag is not None, "Unknown data type!"
                if setflag:    # Set
                    return dict(
                        set_type=infer_types(datavals[0][1][0]),
                        key_type=infer_types(datavals[0][0]),
                        data=datavals,
                    )
                else:       # Param
                    return dict(
                        param_type=infer_types(datavals[0][1]),
                        key_type=infer_types(datavals[0][0]),
                        data=datavals,
                    )
            else:
                return dict(key_type=infer_types(datavals[0][0]), param_type=infer_types(datavals[0][1]), data=datavals)

        elif type(data) is list:
            #
            # Set data
            #
            if type(data[0]) is tuple:
                return dict(
                    set_type=infer_types(data[0]), data=[list(value) for value in data]
                )
            else:
                return dict(set_type=infer_types(data[0]), data=data)

        elif type(data) is tuple:
            #
            # Parameter tuple
            #
            return list(data)

        else:
            #
            # Return simple data: integer, double or string
            #
            return data


def JsonDataPortal(packed_data=None, filename=None, json_string=None, schema="coek"):
    if json_string is not None:
        packed_data = json.loads(json_string)
    elif packed_data is None:
        packed_data = {}

    if schema == "coek":
        return JSONDataPortal_Coek(packed_data, filename=filename)
    elif schema == "pyomo":
        return JSONDataPortal_Pyomo(packed_data, filename=filename)

    raise ValueError("Unexpected JSON schema: " + schema)


def load_data_from_json(*, filename=None, packed_data=None, json_string=None, schema="coek"):
    return JsonDataPortal(filename=filename, packed_data=packed_data, json_string=json_string, schema=schema)
