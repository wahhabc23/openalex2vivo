import logging
from typing import Dict, Any

# Import the core crosswalk executor without executing the argparse/CLI code
from openalex2vivo import default_execute

logger = logging.getLogger(__name__)

class OpenAlexProcessingError(Exception):
    """Custom exception raised when the legacy package fails to process an OpenAlex."""
    pass

class OpenAlexService:
    def __init__(self, use_cache: bool = True, timeout: int = 10, namespace: str = "http://vivo.mydomain.edu/individual/"):
        """
        Initialize the OpenAlex Service.
        :param use_cache: Whether to use caching (stub concept for future use).
        :param timeout: Timeout for remote requests.
        :param namespace: The base VIVO namespace.
        """
        self.config = {
            "use_cache": use_cache,
            "timeout": timeout,
            "namespace": namespace
        }

    def process_openalex(self, orcid_id: str) -> Dict[str, Any]:
        """
        Main programmatic entry point intended for robust frameworks like FastAPI.
        Bypasses the legacy Flask and CLI layers.

        :param orcid_id: The OpenAlex identifier string (e.g. '0000-0002-1825-0097')
        :return: A dictionary containing the standard VIVO RDF output and profile data.
        """
        try:
            # Execute the core component directly
            graph, profile, person_uri = default_execute(
                orcid_id, 
                namespace=self.config["namespace"],
                # We can explicitly pass default variables here rather than relying on argparse
                person_uri=None, 
                person_id=None, 
                skip_person=False, 
                person_class=None
            )

            # Extract the raw graph as Turtle for easy transmission in JSON payload
            vivo_rdf_turtle = graph.serialize(format="turtle")
            # In Python 3, rdflib.serialize might return a bytes string. 
            # We must decode to standard utf-8 string if it is bytes.
            if isinstance(vivo_rdf_turtle, bytes):
                vivo_rdf_turtle = vivo_rdf_turtle.decode('utf-8')

            return {
                "success": True,
                "orcid_id": orcid_id,
                "person_uri": str(person_uri),
                "vivo_rdf": vivo_rdf_turtle,
                "profile_data": profile
            }

        except ValueError as ve:
            # Re-raise known value errors which a FastAPI router could map to HTTP 400
            logger.warning(f"Validation error processing {orcid_id}: {ve}")
            raise ve
        except Exception as e:
            # Wrap all inner unstructured errors in a clean custom exception (HTTP 500)
            logger.error(f"Legacy crosswalk package crashed on {orcid_id}: {str(e)}")
            raise OpenAlexProcessingError(f"Internal processing failed: {str(e)}")
