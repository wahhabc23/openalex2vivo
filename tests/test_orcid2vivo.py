from unittest import TestCase
from rdflib import Graph, URIRef, RDF, OWL
import openalex2vivo_app.vivo_namespace as ns
from openalex2vivo import PersonCrosswalk
from openalex2vivo_app.vivo_namespace import VIVO


class TestPersonCrosswalk(TestCase):
    def setUp(self):
        self.graph = Graph(namespace_manager=ns.ns_manager)
        self.person_uri = ns.D["test"]
        self.openalex_id = "0000-0003-1527-0030"
        self.openalex_id_uriref = URIRef("http://openalex.org/{}".format(self.openalex_id))

    def test_add_openalex_id(self):
        PersonCrosswalk._add_openalex_id(self.person_uri, self.openalex_id, self.graph, False)
        self.assertEqual(2, len(self.graph))

        self.assertTrue((self.person_uri, VIVO.openalexId, self.openalex_id_uriref) in self.graph)
        self.assertTrue((self.openalex_id_uriref, RDF.type, OWL.Thing) in self.graph)

    def test_add_openalex_id_confirmed(self):
        PersonCrosswalk._add_openalex_id(self.person_uri, self.openalex_id, self.graph, True)
        self.assertEqual(3, len(self.graph))

        self.assertTrue((self.openalex_id_uriref, VIVO.confirmedOpenAlexId, self.person_uri) in self.graph)
