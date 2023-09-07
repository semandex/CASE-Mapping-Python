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
            "case-investigation": "https://caseontology.org/ontology/case/investigation#",
            "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
            "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
            "uco-action": "https://unifiedcyberontology.org/ontology/uco/action",
            "uco-core": "https://unifiedcyberontology.org/ontology/uco/core",
            "uco-identity": "https://unifiedcyberontology.org/ontology/uco/identity",
            "uco-location": "https://unifiedcyberontology.org/ontology/uco/location",
            "uco-role": "https://unifiedcyberontology.org/ontology/uco/role",
            "uco-observable": "https://unifiedcyberontology.org/ontology/uco/observable",
            "uco-tool": "https://unifiedcyberontology.org/ontology/uco/tool",
            "uco-types": "https://unifiedcyberontology.org/ontology/uco/types",
            "uco-vocabulary": "https://unifiedcyberontology.org/ontology/uco/vocabulary",
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
