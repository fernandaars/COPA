import requests

BASE_URL = "http://localhost:8000/REST/"


def test_request_pool_all():
    data = dict()

    print(requests.get(BASE_URL + "pools", data).json())


def test_add_container_pool(container_pool="testServer", ip="1.1.1.1"):
    data = {"container_pool": container_pool,
            "ip":             ip,
            "operation":      "add"}

    print(requests.post(BASE_URL + "pools", data).json())


def test_remove_container_pool(container_pool="testServer"):
    if not container_pool:
        container_pool = "testServer"

    data = {"container_pool": container_pool,
            "operation":      "remove"}

    print(requests.post(BASE_URL + "pools", data).json())


def test_get_container_info(container_pool="server1", container="my-container"):
    data = {"container_name": container,
            "container_pool": container_pool,
            "operation":      "information"}

    print(requests.get(BASE_URL + "container", data).json())


def test_start_container(container_pool="server1", container="my-container"):
    data = {"container_name": container,
            "container_pool": container_pool,
            "operation":      "start"}

    print(requests.post(BASE_URL + "container", data).json())


def test_stop_container(container_pool="server1", container="my-container"):
    data = {"container_name": container,
            "container_pool": container_pool,
            "operation":      "stop"}

    print(requests.post(BASE_URL + "container", data).json())


def test_freeze_container(container_pool="server1", container="my-container"):
    data = {"container_name": container,
            "container_pool": container_pool,
            "operation":      "freeze"}

    print(requests.post(BASE_URL + "container", data).json())


def test_unfreeze_container(container_pool="server1", container="my-container"):
    data = {"container_name": container,
            "container_pool": container_pool,
            "operation":      "unfreeze"}

    print(requests.post(BASE_URL + "container", data).json())


def test_delete_container(container_pool="server1", container="my-container"):
    data = {"container_name": container,
            "container_pool": container_pool,
            "operation":      "delete"}

    print(requests.post(BASE_URL + "container", data).json())


def test_create_container(container_pool="server1", container="my-container",
                          image_type="ubuntu"):
    data = {"container_name": container,
            "container_pool": container_pool,
            "operation":      "create",
            "image_type":     image_type}

    print(requests.post(BASE_URL + "container", data).json())


def test_migrate_container(container_pool="server1", container="my-container",
                           dest_pool="server2"):
    data = {"container_name":   container,
            "container_pool":   container_pool,
            "destination_pool": dest_pool,
            "operation":        "migrate"}

    print(requests.post(BASE_URL + "container", data).json())


def test_list_containers(container_pool="server1"):
    data = {"container_pool": container_pool,
            "operation":      "list_containers"}

    print(requests.get(BASE_URL + "container", data).json())


def test_get_image_list():
    data = {}

    print(requests.get(BASE_URL + "image", data).json())


if __name__ == '__main__':
    test_request_pool_all()
    test_add_container_pool()
    test_remove_container_pool()
    test_list_containers()
    test_create_container()
    test_get_container_info()
    test_stop_container()
    test_start_container()
    test_freeze_container()
    test_unfreeze_container()
    test_migrate_container(dest_pool="server3")
    test_delete_container(container_pool="server3")
    test_get_image_list()
    pass
