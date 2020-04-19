import http.client
import urllib.parse


def do_get(protocol, host, url):
    if protocol == "HTTPS":
        conn = http.client.HTTPSConnection(host)
    else:
        conn = http.client.HTTPConnection(host)
    conn.request("GET", url)
    return conn


def do_post(protocol, host, url, params):
    if protocol == "HTTPS":
        conn = http.client.HTTPSConnection(host)
    else:
        conn = http.client.HTTPConnection(host)
    headers = {
        "Content-type": "application/x-www-form-urlencoded",
        "Accept": "text/plain"
    }
    conn.request("POST", url, params, headers)
    return conn


def request(method, protocol, host, url, params):
    conn = None
    try:
        if method == "GET":
            conn = do_get(protocol, host, url)
        elif method == "POST":
            conn = do_post(protocol, host, url, params)
        if conn is not None:
            response = conn.getresponse()
            if response.status // 100 > 3:
                return '{} {}'.format(response.status, response.reason)
            result = response.read()  # read entire content.
            conn.close()
            return result
    except Exception as e:
        return e
    return None


print(request("GET", "HTTPS", "docs.python.org",
              "/3/_sources/library/http.client.txt", ""))

params = urllib.parse.urlencode({
    '@number': 12524,
    '@type': 'issue',
    '@action': 'show'
})
print(request("POST", "HTTP", "bugs.python.org", "", params))
