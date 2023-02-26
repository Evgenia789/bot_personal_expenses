import requests
from bs4 import BeautifulSoup


def get_currency_rate(currency: str) -> float:
    """Get a currency rate"""
    headers = {'User-Agent': ('Mozilla/5.0 (Macintosh; '
                              'Intel Mac OS X 10_15_3) '
                              'AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/80.0.3987.149 Safari/537.36')}
    currency_precision = {"RUB": 2, "RSD": 2, "EUR": 2, "LAR": 2}
    page_name = {
        "RUB": 'https://www.google.com/search?q=%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&sxsrf=AJOqlzUyXAIxjj0SO1Y4tlB8LZlqH9BwFA%3A1677172882939&ei=kqD3Y5L9OIGrrgTG56_gAQ&ved=0ahUKEwiSjqjvk6z9AhWBlYsKHcbzCxwQ4dUDCA8&uact=5&oq=%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQAzIECCMQJzIGCAAQBxAeMgkIABAHEB4Q8QQyBggAEAcQHjIHCAAQgAQQCjIJCAAQBxAeEPEEMgcIABCABBAKMgcIABCABBAKMgcIABCABBAKMgcIABCABBAKOgQIABBDOgoIABCABBAUEIcCOgUIABCABDoJCAAQFhAeEPEEOgcIABANEIAEOgYIABAeEA06CQgAEB4QDRDxBEoECEEYAFAAWM1TYK1caAFwAXgAgAF1iAH6CpIBAzYuOJgBAKABAaABAsABAQ&sclient=gws-wiz-serp',
        "RSD": 'https://www.google.com/search?q=%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80+%D0%BA+%D1%81%D0%B5%D1%80%D0%B1%D1%81%D0%BA%D0%BE%D0%BC%D1%83+%D0%B4%D0%B8%D0%BD%D0%B0%D1%80%D1%83&sxsrf=AJOqlzWQLLIUBfWfHv8k6Q-fEyQX4FMuvQ%3A1677172637776&ei=nZ_3Y6KJL4WEwPAP4Z2i-A0&ved=0ahUKEwjiy7T6kqz9AhUFAhAIHeGOCN8Q4dUDCA8&uact=5&oq=%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80+%D0%BA+%D1%81%D0%B5%D1%80%D0%B1%D1%81%D0%BA%D0%BE%D0%BC%D1%83+%D0%B4%D0%B8%D0%BD%D0%B0%D1%80%D1%83&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQAzIECCMQJzIJCAAQFhAeEPEEOgYIABAHEB46CQgAEAcQHhDxBDoECAAQQzoKCAAQgAQQFBCHAjoFCAAQgAQ6BwgAEIAEEAo6CwgAEAgQBxAeEPEEOggIABAIEAcQHjoJCAAQCBAeEPEEOgUIABCiBDoMCCEQoAEQwwQQChAqOggIIRCgARDDBDoICAAQogQQiwM6BggAEBYQHkoECEEYAFAAWKlwYMl2aAJwAXgAgAH1AogBmhCSAQg0LjEyLjAuMZgBAKABAaABArgBAsABAQ&sclient=gws-wiz-serp',
        "EUR": 'https://www.google.com/search?q=%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80+%D0%BA+%D0%B5%D0%B2%D1%80%D0%BE+&sxsrf=AJOqlzXfJixZQqsFv6OgqLh7h5aHJnjNqg%3A1677172921448&ei=uaD3Y7L8GoX3qwG_5LCIDA&ved=0ahUKEwjyvNaBlKz9AhWF-yoKHT8yDMEQ4dUDCA8&uact=5&oq=%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80+%D0%BA+%D0%B5%D0%B2%D1%80%D0%BE+&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQAzIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQ6BggAEAcQHjoJCAAQBxAeEPEEOgoIABCABBAUEIcCOgQIABBDOgcIABCABBAKOgQIIxAnOgYIABAWEB46CQgAEBYQHhDxBDoGCAAQCBAeOgkIABAIEB4Q8QQ6CwgAEAgQBxAeEPEEOgUIABCiBEoECEEYAFAAWK8rYLAuaABwAXgAgAHpAYgB9gqSAQUyLjguMZgBAKABAaABAsABAQ&sclient=gws-wiz-serp',
        "LAR": 'https://www.google.com/search?q=%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80+%D0%BA+%D0%BB%D0%B0%D1%80%D0%B8&sxsrf=AJOqlzX0H5Xu3se1GBifEw6HC31pskVfww%3A1677172946506&ei=0qD3Y4TPHoGMrwT46b34Dg&ved=0ahUKEwiEgNCNlKz9AhUBxosKHfh0D-8Q4dUDCA8&uact=5&oq=%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80+%D0%BA+%D0%BB%D0%B0%D1%80%D0%B8&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQAzIFCAAQgAQyBQgAEIAEMgUIABCABDIICAAQgAQQywEyCAgAEIAEEMsBMggIABCABBDLATIJCAAQFhAeEPEEMgkIABAWEB4Q8QQyCQgAEBYQHhDxBDIJCAAQFhAeEPEEOgYIABAHEB46CQgAEAcQHhDxBDoECAAQQzoKCAAQgAQQFBCHAjoHCAAQgAQQCjoECCMQJzoJCCMQJxBGEIICSgQIQRgAUABYrBxglyBoAHABeACAAW-IAdAHkgEDNy4zmAEAoAEBwAEB&sclient=gws-wiz-serp'
    }
    full_page = requests.get(page_name[currency], headers=headers)
    soup = BeautifulSoup(full_page.content, 'html.parser')
    convert = soup.findAll("span",
                           {"class": "DFlfde", "class": "SwHCTb",
                            "data-precision": currency_precision[currency]})

    return float(convert[0].text.replace(",", "."))
