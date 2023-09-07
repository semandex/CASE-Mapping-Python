from ..base import ObjectEntity, FacetEntity


class FacetBirthInformation(FacetEntity):
    def __init__(self, birthdate=None):
        """
        :param birthdate: the date of birth of an identity
        """
        super().__init__()
        self["@type"] = "uco-identity:BirthInformationFacet"
        self._datetime_vars(**{"uco-identity:birthdate": birthdate})


class Identity(ObjectEntity):
    def __init__(self, facets=None):
        super().__init__()
        self["@type"] = "uco-identity:Identity"
        self.append_facets(facets)


class FacetSimpleName(FacetEntity):
    def __init__(self, given_name=None, family_name=None):
        """
        :param given_name: Full name of the identity of person
        :param family_name: Family name of identity of person
        """
        super().__init__()
        self["@type"] = "uco-identity:SimpleNameFacet"
        self._str_vars(
            **{
                "uco-identity:givenName": given_name,
                "uco-identity:familyName": family_name,
            }
        )


directory = {
    "uco-identity:BirthInformationFacet": FacetBirthInformation,
    "uco-identity:Identity": Identity,
    "uco-identity:SimpleNameFacet": FacetSimpleName,
}
