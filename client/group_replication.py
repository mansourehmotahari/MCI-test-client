import httpx
import asyncio

async def add_group(client, server, group_id):
    response = await client.post(
        server + "/v1/group",
        json={"groupId": group_id}
    )
    if response.status_code == 201:
        print(f"Group {group_id} created on server: {server}")
        return True

    print(f"Group {group_id} was not created on server: {server}")
    return False


async def delete_group(client, server, group_id):
    await client.request(
        "DELETE",
        server + "/v1/group",
        json={"groupId": group_id}
    )
    print(f"Group {group_id} deleted from server: {server}")


async def send_group_to_servers(group_id, servers):
    created_servers = []

    async with httpx.AsyncClient() as client:
        for server in servers:
            try:
                added = await add_group(client, server, group_id)
                if added:
                    created_servers.append(server)
                else:
                    for created_server in created_servers:
                        try:
                            await delete_group(client, created_server, group_id)
                        except httpx.HTTPError:
                            pass

                    print(f"Failed to create group on server: {server}")
                    return False

            except httpx.HTTPError:
                for created_server in created_servers:
                    try:
                        await delete_group(client, created_server, group_id)
                    except httpx.HTTPError:
                        pass

                print(f"Failed to create group on server: {server}")
                return False

    print("Group was created on all servers successfully")
    return True



servers = ["http://178.63.196.56:7575", "http://178.63.196.56:7576", "http://178.63.196.56:7577"]
group_id = "group1"

if __name__ == "__main__":
    asyncio.run(send_group_to_servers(group_id, servers))
