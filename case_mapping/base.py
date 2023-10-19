import json
from datetime import datetime
from uuid import uuid4


def unpack_args_array(func):
    """
    If Class functionality (e.g. adding facets) must work both by passing args (self.add_facets(args)) and by passing
    lists/tuples (facets=[args]), this function transforms the latter case into the former when used as a decorator.
    """

    def wrapper(self, *args, **kwargs):
        if len(args) == 1 and (isinstance(args[0], list) or isinstance(args[0], tuple)):
            return func(self, *args[0], **kwargs)
        else:
            return func(self, *args, **kwargs)

    return wrapper


class FacetEntity(dict):
    def __init__(self):
        self["@id"] = str(uuid4())

    def __str__(self):
        return json.dumps(self, indent=4)

    def get_id(self):
        return self["@id"]

    def _append_stuff(self, key, *args, refs=False, objects=False):
        if len(args) == 1 and not args[0]:  # True if no objects to append provided
            pass
        else:
            if len(args) and self.get(key) is None:
                self[key] = list()
            elif len(args) and isinstance(
                self[key], dict
            ):  # if single ref add it to list
                self[key] = [self[key]]
            for item in args:
                if isinstance(item, FacetEntity):
                    if refs:
                        self[key].append({"@id": item.get_id(), "@type": item.get("@type")})
                    elif objects:
                        self[key].append(item)
                else:
                    print(f"{item}: NOT A CASE OBJECT")

    def _append_refs(self, key, *args):
        self._append_stuff(key, *args, refs=True)

    def _append_observable_objects(self, key, *args):
        self._append_stuff(key, *args, objects=True)

    def _append_strings(self, key, *args):
        if len(args) and self.get(key) is None:
            self[key] = list()
        for item in args:
            if isinstance(item, str):
                self[key].append(item)
            else:
                print(f"{item}: NOT A STRING")

    def _str_vars(self, **kwargs):
        for key, var in kwargs.items():
            if isinstance(var, str):
                self[key] = var
            else:
                self.__handle_var_type_errors(key, var, "str")

    def _float_vars(self, **kwargs):
        for key, var in kwargs.items():
            if isinstance(var, float):
                self[key] = var
                # self[key] = {"@type": "xsd:decimal", "@value": str(var)}
            elif isinstance(var, int):
                self[key] = float(var)
                # self[key] = {"@type": "xsd:decimal", "@value": str(float(var))}
            else:
                self.__handle_var_type_errors(key, var, "float")

    def _int_vars(self, **kwargs):
        for key, var in kwargs.items():
            if isinstance(var, int):
                self[key] = var
                # self[key] = {"@type": "xsd:integer", "@value": str(var)}
            else:
                self.__handle_var_type_errors(key, var, "int")

    def _bool_vars(self, **kwargs):
        for key, var in kwargs.items():
            if isinstance(var, bool):
                self[key] = var
                # self[key] = {"@type": "xsd:boolean", "@value": var}
            else:
                self.__handle_var_type_errors(key, var, "bool")

    def _datetime_vars(self, **kwargs):
        for key, var in kwargs.items():
            if isinstance(var, datetime):
                tz_info = var.strftime("%z")
                iso_format = var.isoformat() if tz_info else var.isoformat() + "+00:00"
                self[key] = {"@type": "xsd:dateTime", "@value": iso_format}
            else:
                self.__handle_var_type_errors(key, var, "datetime")

    def _nonegative_int_vars(self, **kwargs):
        for key, var in kwargs.items():
            if isinstance(var, int) and not var < 0:
                self[key] =  var
                # self[key] = {"@type": "xsd:nonNegativeInteger", "@value": str(var)}
            else:
                self.__handle_var_type_errors(key, var, "non-negative integer")

    def _node_reference_vars(self, **kwargs):
        for key, var in kwargs.items():
            if isinstance(var, list) or isinstance(var, tuple):
                is_object_entity = [isinstance(item, ObjectEntity) for item in var]
                if all(is_object_entity):
                    self[key] = [{"@id": item.get_id(), "@type": item.get("@type")} for item in var]
                    # self[key] = [{"@id": item.get_id()} for item in var]
                else:
                    self.__handle_list_type_errors(
                        key, var, "ObjectEntity (no @id key)"
                    )
            elif isinstance(var, ObjectEntity):
                self[key] = {"@id": var.get_id(), "@type": var.get("@type")}
                # self[key] = {"@id": var.get_id()}
            else:
                self.__handle_var_type_errors(key, var, "ObjectEntity (no @id key)")

    def _str_list_vars(self, **kwargs):
        for key, var in kwargs.items():
            if isinstance(var, list) or isinstance(var, tuple):
                is_string = [isinstance(item, str) for item in var]
                if all(is_string):
                    self[key] = list(var)
                else:
                    self.__handle_list_type_errors(key, var, "str")
            elif isinstance(var, str):
                self[key] = [var]
            else:
                self.__handle_var_type_errors(key, var, "str")

    @staticmethod
    def __handle_list_type_errors(var_name, var_val, expected_type):
        if len(var_val) == 1 and var_val[0] is None:
            pass
        else:
            print(
                f"One of the items provided for {var_name} is not of type {expected_type}: items provided: {var_val}"
            )
            raise TypeError

    @staticmethod
    def __handle_var_type_errors(var_name, var_val, expected_type):
        if var_val is None:
            pass
        else:
            print(
                f"Value provided for {var_name} is not of type {expected_type}: value provided: {var_val}"
            )
            raise TypeError


class ObjectEntity(FacetEntity):
    @unpack_args_array
    def append_facets(self, *args):
        """
        :param args: A single/tuple of ObservableObjects
        """
        self._append_observable_objects("uco-core:hasFacet", *args)

    @unpack_args_array
    def append_core_objects(self, *args):
        """
        :param args: A single/tuple of ObservableObjects
        """
        self._append_observable_objects("uco-core:object", *args)

    @unpack_args_array
    def append_core_object_refs(self, *args):
        """
        :param args: A single/tuple of ObservableObjects
        """
        self._append_refs("uco-core:object", *args)

    @unpack_args_array
    def append_indexed_items(self, *args):
        """
        :param args: A single/tuple of ObservableObjects
        """

        for key in ["olo:length", "olo:slot"]:
            if self.get(key) is None:
                self[key] = None

        if len(args) == 1 and not args[0]:  # True if no objects to append provided
            pass
        else:
            if len(args) and self["olo:slot"] is None:
                self["olo:slot"] = list()

            current_index = len(self["olo:slot"])

            for item in args:
                if isinstance(item, FacetEntity):
                    new_entry = dict()
                    current_index += 1
                    new_entry["olo:index"] = str(current_index)
                    new_entry["olo:item"] = {"@id": item.get_id()}
                    self["olo:slot"].append(new_entry)
                else:
                    print(f"{item}: NOT A CASE OBJECT")

            self["olo:length"] = str(current_index)
