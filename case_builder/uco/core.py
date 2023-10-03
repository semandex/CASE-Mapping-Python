from ..base import ObjectEntity, unpack_args_array


class Bundle(ObjectEntity):
    def __init__(
        self,
        case_identifier=None,
        uco_core_name=None,
        spec_version=None,
        description=None,
    ):
        """
        The main CASE Object for representing a case and its activities and objects.
        """
        super().__init__()
        self.build = []
        self["@context"] = {
            "@vocab": "http://caseontology.org/core#",
            "case-investigation": "https://ontology.caseontology.org/case/investigation/",
            "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
            "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
            "uco-action": "https://ontology.unifiedcyberontology.org/uco/action/",
            "uco-core": "https://ontology.unifiedcyberontology.org/uco/core/",
            "uco-identity": "https://ontology.unifiedcyberontology.org/uco/identity/",
            "uco-location": "https://ontology.unifiedcyberontology.org/uco/location/",
            "uco-role": "https://ontology.unifiedcyberontology.org/uco/role/",
            "uco-observable": "https://ontology.unifiedcyberontology.org/uco/observable/",
            "uco-tool": "https://ontology.unifiedcyberontology.org/uco/tool/",
            "uco-types": "https://ontology.unifiedcyberontology.org/uco/types/",
            "uco-vocabulary": "https://ontology.unifiedcyberontology.org/uco/vocabulary/",
            "xsd": "http://www.w3.org/2001/XMLSchema#",
        }
        self["@type"] = "uco-core:Bundle"
        self._str_vars(
            **{
                "uco-core:account_name": uco_core_name,
                "uco-core:specVersion": spec_version,
                "uco-core:description": description,
            }
        )

        if case_identifier:
            self["@id"] = case_identifier

    @unpack_args_array
    def append_to_case_graph(self, *args):
        self._append_observable_objects("@graph", *args)

    @unpack_args_array
    def append_to_uco_object(self, *args):
        """
        Add a single/tuple of result(s) to the list of outputs from an action
        :param args: A CASE object, or objects, often an observable. (e.g., one of many devices from a search operation)
        """
        self._append_observable_objects("uco-core:object", *args)

    @unpack_args_array
    def append_to_rdfs_comments(self, *args):
        self._append_strings("rdfs:comment", *args)

    @unpack_args_array
    def append_to_uco_core_description(self, *args):
        self._append_strings("uco-core:description", *args)


directory = {"uco-core:Bundle": Bundle}
