from google.cloud import artifactregistry_v1


class GoogleArtifactRegistry:

    def __init__(self, project: str, registry: str):
        pass

def sample_get_package():
    # Create a client
    client = artifactregistry_v1.ArtifactRegistryClient()

    # Initialize request argument(s)
    request = artifactregistry_v1.GetPackageRequest(
        name="name_value",
    )

    # Make the request
    response = client.get_package(request=request)

    # Handle the response
    print(response)
