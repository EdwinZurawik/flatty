__all__ = ["get_request_headers"]


def get_request_headers():
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,"
        "image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3"
        ";q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
        "Dnt": "1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4)"
        " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97"
        " Safari/537.36",
    }
    return headers
