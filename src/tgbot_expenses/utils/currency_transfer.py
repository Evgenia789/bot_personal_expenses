import requests
from bs4 import BeautifulSoup


def get_currency_rate(currencies: str) -> float:
    """Get a currency exchange rate"""
    headers = {'User-Agent': ('Mozilla/5.0 (Macintosh; '
                              'Intel Mac OS X 10_15_3) '
                              'AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/80.0.3987.149 Safari/537.36')}
    page_name = {
        "EUR/RSD": ["https://www.google.com/search?q=%D0%B5%D0%B2%D1%80%D0%BE+%D0%BA+%D1%81%D0%B5%D1%80%D0%B1%D1%81%D0%BA%D0%B8%D0%B9+%D0%B4%D0%B8%D0%BD%D0%B0%D1%80%D1%83&sxsrf=AJOqlzU-gE1KyiZIp-1zhm8xzitF6ZznIg%3A1677443314912&ei=8sD7Y4-tN8HjsAej7qJg&ved=0ahUKEwiP7qmng7T9AhXBMewKHSO3CAwQ4dUDCA8&uact=5&oq=%D0%B5%D0%B2%D1%80%D0%BE+%D0%BA+%D1%81%D0%B5%D1%80%D0%B1%D1%81%D0%BA%D0%B8%D0%B9+%D0%B4%D0%B8%D0%BD%D0%B0%D1%80%D1%83&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQAzIJCAAQFhAeEPEEMgkIABAWEB4Q8QQyCQgAEBYQHhDxBDoECCMQJzoECAAQQzoGCAAQBxAeOgUIABCABDoKCAAQgAQQFBCHAjoGCAAQFhAeOgwIABCABBANEEYQggJKBAhBGABQAFinXWDQZGgBcAF4AIABd4gBpAmSAQMyLjmYAQCgAQGgAQLAAQE&sclient=gws-wiz-serp", 2],
        "USD/RSD": ["https://www.google.com/search?q=%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80+%D0%BA+%D1%81%D0%B5%D1%80%D0%B1%D1%81%D0%BA%D0%BE%D0%BC%D1%83+%D0%B4%D0%B8%D0%BD%D0%B0%D1%80%D1%83&sxsrf=AJOqlzW8DLfLtlx5axfwt3w6ITNdI6b5fQ%3A1677443355199&ei=G8H7Y8zhC8z3kgWE1JqgDA&ved=0ahUKEwiM28S6g7T9AhXMu6QKHQSqBsQQ4dUDCA8&uact=5&oq=%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80+%D0%BA+%D1%81%D0%B5%D1%80%D0%B1%D1%81%D0%BA%D0%BE%D0%BC%D1%83+%D0%B4%D0%B8%D0%BD%D0%B0%D1%80%D1%83&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQAzIJCCMQJxBGEIICMgkIABAWEB4Q8QQ6BggAEAcQHjoJCAAQBxAeEPEEOgQIABBDOgUIABCABDoKCAAQgAQQFBCHAjoHCAAQgAQQCjoECCMQJzoLCAAQCBAHEB4Q8QQ6CAgAEAgQBxAeOg0IABAFEAcQHhAPEPEEOgkIABAIEB4Q8QQ6CQgAEAUQHhDxBDoHCAAQHhDxBDoJCAAQHhANEPEEOgUIABCiBDoICAAQogQQiwNKBAhBGABQAFieYGC3amgAcAF4AIABf4gB7A2SAQQ3LjEwmAEAoAEBoAECuAECwAEB&sclient=gws-wiz-serp", 2],
        "USD/EUR": ["https://www.google.com/search?q=%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80+%D0%BA+%D0%B5%D0%B2%D1%80%D0%BE&sxsrf=AJOqlzUZ3bffM1YyaLKdtuV8R0RXVOpolQ%3A1677443388640&ei=PMH7Y-vVJsbysAfq4o1A&ved=0ahUKEwjr473Kg7T9AhVGOewKHWpxAwgQ4dUDCA8&uact=5&oq=%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80+%D0%BA+%D0%B5%D0%B2%D1%80%D0%BE&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQAzIECCMQJzIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDoKCAAQRxDWBBCwAzoHCAAQsAMQQzoGCAAQBxAeOgkIABAHEB4Q8QQ6BAgAEEM6CggAEIAEEBQQhwI6BwgAEIAEEAo6CQgjECcQRhCCAjoJCAAQFhAeEPEESgQIQRgAUMERWJI_YIBBaAJwAXgAgAHMAogBsAuSAQc1LjQuMS4xmAEAoAEBoAECyAEKwAEB&sclient=gws-wiz-serp", 2],
        "USD/RUB": ["https://www.google.com/search?q=%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&sxsrf=AJOqlzW-CGqpBOxdJCiyxNYMrWORIWo1fA%3A1677443435995&ei=a8H7Y4KuPMGdsAfY5bfoBA&oq=%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80+%D0%BA+%D1%80&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQARgAMgcIIxCwAxAnMgoIABBHENYEELADMgoIABBHENYEELADMgoIABBHENYEELADMgoIABBHENYEELADMgoIABBHENYEELADMgoIABBHENYEELADMgoIABBHENYEELADMgoIABBHENYEELADSgQIQRgAUABYAGDsBWgBcAF4AIABAIgBAJIBAJgBAMgBCcABAQ&sclient=gws-wiz-serp", 2],
        "EUR/RUB": ["https://www.google.com/search?q=%D0%B5%D0%B2%D1%80%D0%BE+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&sxsrf=AJOqlzUKHwlj5E4FhPDEFOe-SEIPsAqhkQ%3A1677443459295&ei=g8H7Y_fSEcmtkwXPjpG4Bw&oq=%D0%B5%D0%B2%D1%80%D0%BE&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQARgCMgQIIxAnMgQIIxAnMgQIABBDMgQIABBDMgQIABBDMgQIABBDMgQIABBDMgQIABBDMgQIABBDMgQIABBDSgQIQRgAUABYAGC8E2gAcAF4AIABWYgBWZIBATGYAQCgAQHAAQE&sclient=gws-wiz-serp", 2]
    }

    full_page = requests.get(page_name[currencies][0], headers=headers)
    soup = BeautifulSoup(full_page.content, 'html.parser')
    convert = soup.findAll("span",
                           {"class": "DFlfde", "class": "SwHCTb",
                            "data-precision": page_name[currencies][1]})

    return float(convert[0].text.replace(",", "."))
