from ..base import FacetEntity, unpack_args_array


class FacetActionReferences(FacetEntity):
    def __init__(
        self,
        performer=None,
        instrument=None,
        location=None,
        environment=None,
        results=None,
        objects=None,
    ):
        """
        An action reference contains the details of an InvestigativeAction.
        It groups the properties characterizing the core elements (who, how, with what, where, etc.) for actions.
        The properties consist of identifier references to separate UCO objects detailing the particular property.
        :param performer: The name or id of the person conducting the action
        :param instrument: The tool used to conduct the action
        :param location: The general location where the action took place (Room, Building or Town)
        :param environment: The type of environment (lab, office)
        :param results: A list of resulting output identifiers
        """
        super().__init__()
        self["@type"] = "uco-action:ActionReferencesFacet"
        self._str_vars(**{"uco-action:environment": environment})
        self._node_reference_vars(
            **{
                "uco-action:performer": performer,
                "uco-action:instrument": instrument,
                "uco-action:location": location,
                "uco-action:result": results,
                "uco-action:object": objects,
            }
        )

    @unpack_args_array
    def append_results(self, *args):
        """
        Add result(s) to the list of outputs from an action
        :param args: A CASE object, or objects, often an observable. (e.g., one or many devices from a search operation)
        """
        self._append_refs("uco-action:result", *args)

    @unpack_args_array
    def append_objects(self, *args):
        """
        Add object(s) to the list of outputs from an action
        :param args: A CASE object, or objects, often an observable. (e.g., one or many devices from a search operation)
        """
        self._append_refs("uco-action:object", *args)


directory = {"uco-action:ActionReferencesFacet": FacetActionReferences}
