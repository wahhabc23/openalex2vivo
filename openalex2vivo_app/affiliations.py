from .vivo_namespace import VIVO, OBO
from rdflib import RDFS, RDF, Literal
from .vivo_namespace import FOAF
from .vivo_uri import to_hash_identifier
from .utility import add_date, add_date_interval
import openalex2vivo_app.vivo_namespace as ns


class AffiliationsCrosswalk:
    def __init__(self, identifier_strategy, create_strategy):
        self.identifier_strategy = identifier_strategy
        self.create_strategy = create_strategy

    def crosswalk(self, openalex_profile, person_uri, graph):
        affiliations = openalex_profile.get("affiliations") or []
        for affil in affiliations:
            institution = affil.get("institution", {})
            organization_name = institution.get("display_name")
            if not organization_name:
                continue

            years = affil.get("years", [])
            start_year = str(min(years)) if years else None
            end_year = str(max(years)) if years else None

            # Organization
            organization_uri = self.identifier_strategy.to_uri(FOAF.Organization, {"name": organization_name})
            if self.create_strategy.should_create(FOAF.Organization, organization_uri):
                graph.add((organization_uri, RDF.type, FOAF.Organization))
                graph.add((organization_uri, RDFS.label, Literal(organization_name)))

            # Position
            position_uri = self.identifier_strategy.to_uri(VIVO.Position,
                                                           {"organization_name": organization_name,
                                                            "person_uri": str(person_uri)})
            graph.add((position_uri, RDF.type, VIVO.Position))
            graph.add((position_uri, RDFS.label, Literal("Affiliate")))
            
            # Relates Person and Organization
            graph.add((position_uri, VIVO.relates, person_uri))
            graph.add((position_uri, VIVO.relates, organization_uri))

            # Interval
            if start_year or end_year:
                add_date_interval(position_uri, graph, self.identifier_strategy,
                                  add_date(start_year, graph, self.identifier_strategy) if start_year else None,
                                  add_date(end_year, graph, self.identifier_strategy) if end_year else None)
