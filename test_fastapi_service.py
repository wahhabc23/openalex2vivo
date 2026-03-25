from openalex2vivo_app.fastapi_service import OpenAlexService

def main():
    service = OpenAlexService(use_cache=False)
    # Using a known public OpenAlex for testing
    test_openalex = "0000-0002-1825-0097"
    
    print(f"Testing OpenAlexService wrapper with OpenAlex: {test_openalex}")
    try:
        result = service.process_openalex(test_openalex)
        print("Success! Response keys:", result.keys())
        print("Profile Data Keys:", result["profile_data"].keys())
        # Print a snippet of the RDF
        print("RDF Snippet:", result["vivo_rdf"][:200] + "...")
    except Exception as e:
        print("Error processing OpenAlex:", e)

if __name__ == "__main__":
    main()
