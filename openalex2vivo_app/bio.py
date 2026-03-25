from .vivo_namespace import VIVO
from rdflib import RDFS, RDF, Literal, URIRef, OWL
from .vivo_namespace import VCARD, OBO, FOAF


class BioCrosswalk:
    def __init__(self, identifier_strategy, create_strategy):
        self.identifier_strategy = identifier_strategy
        self.create_strategy = create_strategy

    def crosswalk(self, openalex_profile, person_uri, graph, person_class=FOAF.Person):

        # Get name (OpenAlex provides a single display_name)
        full_name = openalex_profile.get("display_name")

        if full_name and self.create_strategy.should_create(person_class, person_uri):
            # Add person
            graph.add((person_uri, RDF.type, person_class))
            graph.add((person_uri, RDFS.label, Literal(full_name)))

        # Add ORCID as identifier if it exists
        orcid_url = openalex_profile.get("orcid")
        if orcid_url:
            # Clean the URL to ensure VIVO doesn't double-prepend
            clean_orcid = orcid_url.replace("https://orcid.org/", "").replace("http://orcid.org/", "")
            orcid_id_uriref = URIRef(f"http://orcid.org/{clean_orcid}")
            
            # Use confirmedOrcidId to eliminate the 'pending confirmation' UI flag
            graph.add((person_uri, VIVO.orcidId, orcid_id_uriref))
            graph.add((person_uri, VIVO.confirmedOrcidId, orcid_id_uriref))
            graph.add((orcid_id_uriref, RDF.type, OWL.Thing))

        # Following is vcard bio information
        # Add main vcard
        vcard_uri = self.identifier_strategy.to_uri(VCARD.Individual, {"person_uri": person_uri})
        add_main_vcard = False

        # Name vcard
        vcard_name_uri = self.identifier_strategy.to_uri(VCARD.Name, {"person_uri": person_uri})
        if full_name and self.create_strategy.should_create(VCARD.Name, vcard_name_uri):
            graph.add((vcard_name_uri, RDF.type, VCARD.Name))
            graph.add((vcard_uri, VCARD.hasName, vcard_name_uri))
            
            # Since OpenAlex doesn't split names, we can try to separate first and last by first space
            name_parts = full_name.split(" ", 1)
            if len(name_parts) == 2:
                graph.add((vcard_name_uri, VCARD.givenName, Literal(name_parts[0])))
                graph.add((vcard_name_uri, VCARD.familyName, Literal(name_parts[1])))
            else:
                graph.add((vcard_name_uri, VCARD.familyName, Literal(full_name)))
            add_main_vcard = True

        if add_main_vcard and self.create_strategy.should_create(VCARD.Individual, vcard_uri):
            graph.add((vcard_uri, RDF.type, VCARD.Individual))
            # Contact info for
            graph.add((vcard_uri, OBO.ARG_2000029, person_uri))
