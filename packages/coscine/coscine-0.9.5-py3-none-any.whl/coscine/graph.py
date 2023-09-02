###############################################################################
# Coscine Python SDK
# Copyright (c) 2018-2023 RWTH Aachen University
# Licensed under the terms of the MIT License
###############################################################################
# Coscine, short for Collaborative Scientific Integration Environment, is
# a platform for research data management (RDM).
# For more information on Coscine visit https://www.coscine.de/.
#
# Please note that this python module is open source software primarily
# developed and maintained by the scientific community. It is not
# an official service that RWTH Aachen provides support for.
###############################################################################

###############################################################################
# File description
###############################################################################

"""
This file provides a simple wrapper around Coscine application profiles.
It abstracts the interaction with rdf graphs using rdflib and
provides a more intuitive, Coscine-specific interface to these graphs.
"""

###############################################################################
# Dependencies
###############################################################################

from __future__ import annotations
from typing import TYPE_CHECKING, Dict, List
import rdflib
if TYPE_CHECKING:
    from coscine.client import Client

###############################################################################
# Classes / Functions / Scripts
###############################################################################

class ApplicationProfile:
    """
    The ApplicationProfile class serves as a wrapper around Coscine
    application profiles. Coscine application profiles are served
    as rdf graphs which are difficult to interact with, without 3rd
    party libraries.
    The ApplicationProfile class abstracts this interaction.

    Attributes
    ----------
    graph : rdflib.Graph
        An rdf graph parsed with the help of rdflib
    RDFTYPE : str
        A variable frequently used by methods of this class.
    """

    client: Client
    graph: rdflib.Graph
    RDFTYPE: str = "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"

###############################################################################

    def __init__(self, client: Client, graph: str, format: str = "json-ld") -> None:
        """
        Initializes an instance of the ApplicationProfile wrapper class.

        Parameters
        ----------
        graph : str
            A Coscine application profile rdf graph in json-ld text format.
        format : str (optional), default: "json-ld"
            The format of the graph
        """

        self.client = client
        self.graph = rdflib.Graph()
        self.graph.bind("sh", "http://www.w3.org/ns/shacl#")
        self.graph.bind("dcterms", "http://purl.org/dc/terms/")
        self.graph.parse(data=graph, format=format)
        self._recursive_import()

###############################################################################

    def _recursive_import(self):
        """
        Imports parent application profiles
        TODO: Import after importing (actually recurse)
        Currently we just iterate over owl:imports once,
        but after importing new profiles, new owl:imports
        may have appeared in the graph...
        """
        query = "SELECT ?url WHERE { ?_ owl:imports ?url . }"
        for result in self.graph.query(query):
            url = str(result[0])
            profile = self.client.vocabularies.application_profile(url)
            self.graph.parse(data=str(profile), format="ttl")

###############################################################################

    def __str__(self) -> str:
        """
        Serializes the application profile rdf graph used internally
        for easy output to stdout.
        """
        # Explicitly return as str because pylint does not understand
        # rdflib's ambiguous return type for this method.
        return str(self.graph.serialize(format="ttl"))

###############################################################################

    def target(self) -> str:
        """
        Returns a str indicating the target class of the application profile.
        This may for example be "engmeta" in case of an engmeta profile.
        """

        query = \
            """
            SELECT ?target WHERE {
                ?target a sh:NodeShape .
            }
            """
        result = self.query(query)
        return str(result[0][0])  # Force string

###############################################################################

    def query(self, query: str, **kwargs) -> List[List[object]]:
        """
        Performs a SPARQL query against the application profile and
        returns the result as a list of rows.
        """

        items = []
        results = self.graph.query(query, **kwargs)
        for row in results:
            item = []
            for val in row:
                value = val.toPython() if val is not None else None
                item.append(value)
            items.append(item)
        return items

###############################################################################

    def items(self) -> List[dict]:
        """
        Returns all items contained within the application profile as a list
        of key value pairs in their order of appearance.
        """

        query = \
            """
            SELECT ?path ?name ?order ?class ?minCount ?maxCount ?datatype
                (lang(?name) as ?lang)
                (GROUP_CONCAT(?in; SEPARATOR="~,~") as ?ins)
            WHERE {
                ?_ sh:path ?path ;
                    sh:name ?name .
                OPTIONAL { ?_ sh:order ?order . } .
                OPTIONAL { ?_ sh:class ?class . } .
                OPTIONAL { ?_ sh:minCount ?minCount . } .
                OPTIONAL { ?_ sh:maxCount ?maxCount . } .
                OPTIONAL { ?_ sh:datatype ?datatype . } .
                OPTIONAL { ?_ sh:in/rdf:rest*/rdf:first ?in . } .
            }
            GROUP BY ?name
            ORDER BY ASC(?order)
            """
        items: Dict[str, Dict] = {}
        results = self.query(query)
        for result in results:
            lang: str = str(result[7])
            path: str = str(result[0])
            selection: str = str(result[8])
            name: str = str(result[1])
            properties = {
                "path": result[0],
                "name": {
                    "de": name,
                    "en": name
                },
                "order": result[2],
                "class": result[3],
                "minCount": result[4] if result[4] else 0,
                "maxCount": result[5] if result[5] else 42,
                "datatype": result[6],
                "in": selection.split("~,~") if selection else None
            }
            if path not in items:
                items[path] = properties
            else:  # Apply name in different language
                items[path]["name"][lang] = name

        return list(items.values())

###############################################################################

    def length(self) -> int:
        """
        Returns the number of fields contained within the application profile.
        """

        query = \
            """
            SELECT ?path WHERE {
                ?_ sh:path ?path ;
                    sh:order ?order .
            }
            """
        results = self.query(query)
        return len(results)

###############################################################################
