from lib.router.router import SimpleAPI
from insert.service import service
import json
from urllib.parse import parse_qs

app = SimpleAPI()


@app.route("/factorial", methods=['GET'])
async def handle_factorial(scope, receive, send):
    query_string = scope.get('query_string', b'').decode('utf-8')
    query_params = parse_qs(query_string)

    if 'n' not in query_params:
        await app.send_422(send)
        return

    try:
        n = int(query_params['n'][0])
        if n < 0:
            await app.send_400(send)
            return
    except (ValueError, IndexError):
        await app.send_422(send)
        return

    result = service.factorial(n)
    await app.send_json(send, {"result": result})


@app.route("/fibonacci/{n}", methods=['GET'])
async def handle_fibonacci(scope, receive, send):
    path_params = scope.get('path_params', {})
    n_str = path_params.get('n')

    if n_str is None:
        await app.send_422(send)
        return

    try:
        n = int(n_str)
        if n < 0:
            await app.send_400(send)
            return
    except ValueError:
        await app.send_422(send)
        return

    result = service.fibonacci(n)
    await app.send_json(send, {"result": result})


@app.route("/mean", methods=['GET'])
async def handle_mean(scope, receive, send):
    body_bytes = await app.get_request_body(receive)
    if not body_bytes:
        await app.send_422(send)
        return

    try:
        body_str = body_bytes.decode('utf-8')
        data = json.loads(body_str)
        if not isinstance(data, list):
            raise ValueError
        if not data:
            await app.send_400(send)
            return
        floats = []
        for item in data:
            if isinstance(item, (int, float)):
                floats.append(float(item))
            else:
                raise ValueError
        mean_value = service.mean(floats)
        await app.send_json(send, {"result": mean_value})
    except (json.JSONDecodeError, ValueError):
        await app.send_422(send)


if __name__ == "__main__":
    app.run()
