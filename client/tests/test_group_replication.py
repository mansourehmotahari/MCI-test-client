import asyncio

import httpx

import group_replication


def test_add_group_success():
    class Client:
        async def post(self, url, json):
            return httpx.Response(201)

    result = asyncio.run(group_replication.add_group(Client(), "http://178.63.196.56:7575", "group1"))

    assert result is True


def test_add_group_failure():
    class Client:
        async def post(self, url, json):
            return httpx.Response(400)

    result = asyncio.run(group_replication.add_group(Client(), "http://178.63.196.56:7575", "group1"))

    assert result is False


def test_delete_group():
    class Client:
        def __init__(self):
            self.deleted_url = ""

        async def request(self, method, url, json):
            self.deleted_url = url
            return httpx.Response(200)

    client = Client()
    asyncio.run(group_replication.delete_group(client, "http://178.63.196.56:7575", "group1"))

    assert client.deleted_url == "http://178.63.196.56:7575/v1/group"


def test_send_group_to_servers_success(monkeypatch):
    class Client:
        async def __aenter__(self):
            return self

        async def __aexit__(self, type, value, traceback):
            pass

        async def post(self, url, json):
            return httpx.Response(201)

        async def request(self, method, url, json):
            return httpx.Response(200)

    monkeypatch.setattr(group_replication.httpx, "AsyncClient", Client)

    result = asyncio.run(
        group_replication.send_group_to_servers(
            "group1", ["http://178.63.196.56:7575", "http://178.63.196.56:7576"]
        )
    )

    assert result is True


def test_send_group_to_servers_delete_when_server_fails(monkeypatch):
    deleted_servers = []

    class Client:
        async def __aenter__(self):
            return self

        async def __aexit__(self, type, value, traceback):
            pass

        async def post(self, url, json):
            if "http://178.63.196.56:7576" in url:
                return httpx.Response(400)
            return httpx.Response(201)

        async def request(self, method, url, json):
            deleted_servers.append(url)
            return httpx.Response(200)

    monkeypatch.setattr(group_replication.httpx, "AsyncClient", Client)

    result = asyncio.run(
        group_replication.send_group_to_servers(
            "group1", ["http://178.63.196.56:7575", "http://178.63.196.56:7576"]
        )
    )

    assert result is False
    assert deleted_servers == ["http://178.63.196.56:7575/v1/group"]
