import requests
from bs4 import BeautifulSoup


def get_currency_rate(currency: str) -> int:
    """Get a currency rate"""
    headers = {'User-Agent': ('Mozilla/5.0 (Macintosh; '
                              'Intel Mac OS X 10_15_3) '
                              'AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/80.0.3987.149 Safari/537.36')}
    currency_precision = {"RUB": 3, "RSD": 4, "EUR": 2, "LAR": 2}
    page_name = {
        "RUB": 'https://www.google.com/search?q=%D1%80%D1%83%D0%B1%D0%BB%D1%8C+%D0%BA+%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80%D1%83&sxsrf=ALiCzsaGJX6v7VIY3fDUk2jqZtwJ7l5YiA%3A1672762983085&ei=Z1a0Y9_aBLW-xc8PrbKM2A8&ved=0ahUKEwifqpnb56v8AhU1X_EDHS0ZA_sQ4dUDCA8&uact=5&oq=%D1%80%D1%83%D0%B1%D0%BB%D1%8C+%D0%BA+%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80%D1%83&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQAzIJCAAQQxBGEIICMgQIABBDMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQ6CggAEEcQ1gQQsAM6BwgAELADEEM6DAgAEIAEEA0QRhCCAjoHCAAQgAQQDToHCCMQ6gIQJzoNCC4QxwEQrwEQ6gIQJzoNCC4QxwEQ0QMQ6gIQJzoMCAAQ6gIQtAIQQxgBOgoIABCABBCHAhAUOgsILhCABBDHARDRAzoICC4QgAQQ1AI6BQguEIAEOg8IABCABBCHAhAUEEYQggI6BwgAEIAEEApKBAhBGABKBAhGGAFQtQRYvjpgtEVoA3ABeASAAdkDiAGQIpIBCjAuMTUuNS4wLjGYAQCgAQGwARTIAQrAAQHaAQYIARABGAE&sclient=gws-wiz-serp',
        "RSD": 'https://www.google.com/search?q=%D1%81%D0%B5%D1%80%D0%B1%D1%81%D0%BA%D0%B8%D0%B9+%D0%B4%D0%B8%D0%BD%D0%B0%D1%80+%D0%BA+%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80%D1%83&sxsrf=ALiCzsbg9DzexTWHGU0SVNUYska4XFEAyA%3A1672768858383&ei=Wm20Y8_sFr-I9u8Pi8KMKA&ved=0ahUKEwjPgeHM_av8AhU_hP0HHQshAwUQ4dUDCA8&uact=5&oq=%D1%81%D0%B5%D1%80%D0%B1%D1%81%D0%BA%D0%B8%D0%B9+%D0%B4%D0%B8%D0%BD%D0%B0%D1%80+%D0%BA+%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80%D1%83&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQAzIHCAAQgAQQDTIHCAAQgAQQDTIGCAAQBRAeMgYIABAFEB4yBggAEAUQHjoKCAAQRxDWBBCwAzoHCAAQsAMQQzoMCCMQsAIQJxBGEIICOgYIABAHEB46CAgAEAgQBxAeOgoIABAIEAcQHhAPOgYIABAeEA06CAgAEAUQHhANOggIABAFEAcQHkoECEEYAEoECEYYAFCmAljxDmDyE2gBcAF4AYABiAWIAdAPkgELMC43LjAuMS4wLjGYAQCgAQHIAQrAAQE&sclient=gws-wiz-serp',
        "EUR": 'https://www.google.com/search?q=%D0%B5%D0%B2%D1%80%D0%BE+%D0%BA+%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80%D1%83&sxsrf=ALiCzsbC1eXze_ugmPGJH2J48KYIVOotOA%3A1672768866008&ei=Ym20Y48Ti5f27w_Kh56gBQ&ved=0ahUKEwiPzLLQ_av8AhWLi_0HHcqDB1QQ4dUDCA8&uact=5&oq=%D0%B5%D0%B2%D1%80%D0%BE+%D0%BA+%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80%D1%83&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQAzIECAAQQzIECAAQQzIECAAQQzIGCAAQBxAeMgcIABCABBANMgYIABAHEB4yBwgAEIAEEA0yBwgAEIAEEA0yBwgAEIAEEA0yBwgAEIAEEA06CggAEEcQ1gQQsAM6BwgAELADEENKBAhBGABKBAhGGABQlwxYjxBghBloAXABeACAAZQCiAGQBpIBBTAuMy4xmAEAoAEByAEKwAEB&sclient=gws-wiz-serp',
        "LAR": 'https://www.google.com/search?q=%D0%BB%D0%B0%D1%80%D0%B8+%D0%BA+%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80%D1%83&sxsrf=ALiCzsYtpkSPdbiryc-rXSJLBA6RBM5A0A%3A1672819411717&ei=0zK1Y4O0K9mLi-gP-tGniAU&ved=0ahUKEwjD6bv2ua38AhXZxQIHHfroCVEQ4dUDCA8&uact=5&oq=%D0%BB%D0%B0%D1%80%D0%B8+%D0%BA+%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80%D1%83&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQAzIECAAQQzIECAAQQzIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIICAAQgAQQywEyCAgAEIAEEMsBOgYIABAHEB46BwgAEIAEEAo6CAgAEAUQBxAeSgQIQRgASgQIRhgAUABY0gNg3wdoAHABeACAAdUCiAGVBpIBBzAuMy4wLjGYAQCgAQHAAQE&sclient=gws-wiz-serp'
    }

    full_page = requests.get(page_name[currency], headers=headers)
    soup = BeautifulSoup(full_page.content, 'html.parser')
    convert = soup.findAll("span",
                           {"class": "DFlfde", "class": "SwHCTb",
                            "data-precision": currency_precision[currency]})

    return float(convert[0].text.replace(",", "."))
