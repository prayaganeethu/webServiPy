import server


def build_routes():
    server.add_route('get', '/home', home)
    server.add_route('get', '/welcome', welcome)


def home(request, response):
    data = request["content"]['a']
    print(data)
    return server.send_html_handler(request, response, data)


def welcome(request, response):
    data = """
<form action='/home' method='get'>
<input type='text' name='a'/>
<input type='text' name='b'/>
<button type='submit'>submit</button>
</form>
"""

    return server.send_html_handler(request, response, data)


if __name__ == "__main__":
    build_routes()
    server.start_server("localhost", 5555)
