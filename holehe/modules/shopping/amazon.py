from holehe.core import *
from holehe.localuseragent import *


async def amazon(email, client, out):
    name = "amazon"

    headers = {"User-agent": random.choice(ua["browsers"]["chrome"])}
    url = "https://www.amazon.com/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.com%2F%3F_encoding%3DUTF8%26ref_%3Dnav_ya_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=usflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&"
    req = await client.get(url, headers=headers)
    body = BeautifulSoup(req.text, 'html.parser')
    data = dict([(x["name"], x["value"]) for x in body.select(
        'form input') if ('name' in x.attrs and 'value' in x.attrs)])
    data["email"] = email
    req = await client.post(f'https://www.amazon.com/ap/signin/', data=data)
    body = BeautifulSoup(req.text, 'html.parser')
    if body.find("div", {"id": "auth-password-missing-alert"}):
        out.append({"name": name,
                    "rateLimit": False,
                    "exists": True,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
    else:
        out.append({"name": name,
                    "rateLimit": False,
                    "exists": False,
                    "emailrecovery": None,
                    "phoneNumber": None,
                    "others": None})
