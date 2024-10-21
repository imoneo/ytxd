from urllib.parse import urlparse, parse_qs, urlencode, urlunparse


def remove_playlist_context(url: str) -> str:
    # Parse the URL and its query parameters
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)

    # Remove the 'list' parameter if it exists
    if "list" in query_params:
        del query_params["list"]

    # Rebuild the query string without the 'list' parameter
    new_query = urlencode(query_params, doseq=True)

    # Construct the new URL without the playlist
    new_url = urlunparse(
        (
            parsed_url.scheme,
            parsed_url.netloc,
            parsed_url.path,
            parsed_url.params,
            new_query,
            parsed_url.fragment,
        )
    )

    return new_url


def is_youtube_playlist(url: str) -> bool:
    parsed_url = urlparse(url)

    # Check if the URL is from youtube.com and the path is /playlist
    if "youtube.com" in parsed_url.netloc and parsed_url.path == "/playlist":
        query_params = parse_qs(parsed_url.query)
        # Check if the 'list' parameter exists
        if "list" in query_params:
            return True
    return False
