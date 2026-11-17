# Partea 1

import requests
BASE = "https://httpbin.org"
PATHS = ["/get", "/redirect/2", "/delay/1", "/status/404", "/delay/5"]

def search(params):
    r = requests.get(BASE + "/get", params=params, timeout=10)
    r.raise_for_status()
    return r.json()["args"]

def search_url(params):
    r = requests.get(BASE + "/get", params=params, timeout=10)
    r.raise_for_status()
    return r.url

# Partea 2

def fetch_with_agent(agent):
    r = requests.get(
        BASE + "/headers",
        headers={"User-Agent": agent},
        timeout=10
    )
    r.raise_for_status()
    return r.json()["headers"]["User-Agent"]

def default_agent():
    r = requests.get(BASE + "/headers", timeout=10)
    r.raise_for_status()
    return r.json()["headers"]["User-Agent"]

# Partea 3

def post_json(data):
    r = requests.post(
        BASE + "/post",
        json=data,
        timeout=10
    )
    r.raise_for_status()
    return r.json()["json"]

def post_form(data):
    r = requests.post(
        BASE + "/post",
        data=data,
        timeout=10
    )
    r.raise_for_status()
    return r.json()["form"]

# Partea 4

def describe_status(code):
    r = requests.get(BASE + f"/status/{code}", timeout=10)
    if 200 <= r.status_code < 300:
        return "succes"
    if 400 <= r.status_code < 500:
        return "eroare client"
    if 500 <= r.status_code < 600:
        return "eroare server"
    return "necunoscut"

def is_ok(code):
    try:
        r = requests.get(BASE + f"/status/{code}", timeout=10)
        r.raise_for_status()
        return True
    except requests.RequestException:
        return False

# Partea 5

def count_redirects(n):
    r = requests.get(BASE + f"/redirect/{n}", timeout=10)
    r.raise_for_status()
    return len(r.history)

def final_url(n):
    r = requests.get(BASE + f"/redirect/{n}", timeout=10)
    r.raise_for_status()
    return r.url

def first_hop(n):
    r = requests.get(
        BASE + f"/redirect/{n}",
        allow_redirects=False,
        timeout=10
    )
    return r.headers.get("Location")

# Partea 6

def cookie_demo(name, value):
    with requests.Session() as s:
        s.get(
            BASE + "/cookies/set",
            params={name: value},
            timeout=10
        )
        r = s.get(BASE + "/cookies", timeout=10)
        r.raise_for_status()
        return r.json()["cookies"]

def no_session_demo(name, value):
    requests.get(
        BASE + "/cookies/set",
        params={name: value},
        timeout=10
    )
    r = requests.get(BASE + "/cookies", timeout=10)
    r.raise_for_status()
    return r.json()["cookies"]

# Partea 7

def report(path):
    try:
        r = requests.get(BASE + path, timeout=3)
        return {
            "status": r.status_code,
            "final_url": r.url,
            "redirects": len(r.history),
            "seconds": r.elapsed.total_seconds(),
            "content_type": r.headers.get("Content-Type", "").split(";")[0]
        }
    except requests.RequestException as e:
        return {
            "status": None,
            "error": str(e)
        }

# Partea 8

def check_login(user, password):
    try:
        r = requests.get(
            BASE + "/basic-auth/admin/secret",
            auth=(user, password),
            timeout=10
        )
        return r.status_code == 200
    except requests.RequestException:
        return False

if __name__ == "__main__":
    # Teste Partea 1
    print(search({"q": "python", "page": "2"}))
    print(search({"q": "hello world & co"}))
    print(search_url({"q": "python", "page": "2"}))

    # Teste Partea 2
    print(fetch_with_agent("MyBot/1.0"))
    print(default_agent())

    # Teste Partea 3
    print(post_json({"name": "Ana", "age": 19, "tags": ["a", "b"]}))
    print(post_form({"user": "ana", "city": "Bălți"}))

    # Teste Partea 4
    print(describe_status(200))
    print(describe_status(404))
    print(describe_status(503))
    print(is_ok(204))
    print(is_ok(500))

    # Teste Partea 5
    print(count_redirects(3))
    print(final_url(2))
    print(first_hop(3))

    # Teste Partea 6
    print(cookie_demo("theme", "dark"))
    print(no_session_demo("theme", "dark"))

    # Teste Partea 8
    print(check_login("admin", "secret"))
    print(check_login("admin", "gresit"))