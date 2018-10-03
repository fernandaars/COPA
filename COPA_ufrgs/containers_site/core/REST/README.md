# COPA Containers REST API #

## Available functions ##

| Function                | URI              | Method                  |
| :---------------------- | :--------------- | :---------------------: |
| [Pool](#pool)           | /REST/pools/     | [GET](#pool-get)        |
|                         |                  | [POST](#pool-post)      |
| [Container](#container) | /REST/container/ | [GET](#container-get)   |
|                         |                  | [POST](#container-post) |
| [Image](#pool)          | /REST/image/     | [GET](#image-get)       |

#### Pool ####
##### Pool: GET #####
* **Description:**     Requests a list of existing Container Pools
* **Required Parameters:** -
* **Optional Parameters:** -
* **Returns:**
    - SUCCESS: ``{'pools': [[pool, ip],...], 'success': 'pools'}``
    - WARNING: -
    - ERROR: ``{'error': str(error Description)}``
* **Usage Example:**

```python
In [0]: data = dict()
In [1]: result = requests.get(BASE_URL + "pools/", data).json()
In [2]: print(result)
Out[2]: {'pools': [['server1', '192.168.122.15'], ['server3', '192.168.122.250']], 'success': 'pools'}
```

##### Pool: POST #####
* **Description:** Execute both add and delete container pools operations
* **Required Parameters:**
    * `"operation"`: `"add"`, `"delete"`
    * `"container_pool"`: Pool name
    * `"ip"` - Only for `"add"`: IPv4 of the new container pool.
* **Optional Parameters:** -
* **Returns:**
    - SUCCESS:
        + `add`: ``{'container_pool': <POOL_NAME>, 'local_ip': <POOL_IP>, 'success': 'Container pool added Successfully'}``
        + `remove`: ``{'container_pool': <POOL_NAME>, 'success': 'Container pool removed successfully.'}``
    - WARNING: -
    - ERROR: ``{'error': str(error Description)}``
* **Usage Example:**

```python
In [0]: data = {"container_pool": 'testServer',
               "ip":             '1.1.1.1',
               "operation":      "add"}
In [1]: result = requests.post(BASE_URL + "pools/", data).json()
In [2]: print(result)
Out[2]: {'container_pool': 'testServer',
         'local_ip': '1.1.1.1',
         'success': 'Container pool added Successfully'}
```

```python
In [0]: data = {"container_pool": 'testServer',
               "operation":      "remove"}
In [1]: result = requests.post(BASE_URL + "pools/", data).json()
In [2]: print(result)
Out[2]: {'container_pool': 'testServer',
         'success': 'Container pool removed successfully.'}
```

#### Container ####
##### Container: GET #####
* **Description:** Gets information about containers: hardware, network.
                   Also lists the containers available in a Container Pool.
* **Required Parameters:**
    * ``"container_pool"``: Container pool name.
    * ``"operation"``: Desired operation (``"information"``, ``"list_containers"``).
* **Optional Parameters:**
    * ``"container_name"``: If specified, will get the information of one container only.
* **Returns:**
    - WARNING: specially for Container information (LXC<2.19)(``'warning': "'ContainerState' object has no attribute 'cpu'"``)
    - ERROR: ``{'error': str(error Description)}``
    - SUCCESS:
        + ``"list_containers"``: ``{'containers': [<LIST OF CONTAINER NAMES>]}``
        + ``"information"``: 
        
        ```python
            {'disk': {},
             'memory': {'usage': 141582336, 'usage_peak': 141582336, 'swap_usage': 0, 'swap_usage_peak': 0},
             'network': {'eth0': {'addresses': [{'family': 'inet', 'address': '192.168.122.14', 'netmask': '24', 'scope': 'global'},
                                                {'family': 'inet6', 'address': 'fe80::216:3eff:feed:a5bf', 'netmask': '64', 'scope': 'link'}],
                                  'counters': {'bytes_received': 9684, 'bytes_sent': 558, 'packets_received': 129, 'packets_sent': 7},
                                  'hwaddr': '00:16:3e:ed:a5:bf',
                                  'host_name': 'veth8WD1SA',
                                  'mtu': 1500,
                                  'state': 'up',
                                  'type': 'broadcast'},
                         'lo': {'addresses': [{'family': 'inet', 'address': '127.0.0.1', 'netmask': '8', 'scope': 'local'},
                                              {'family': 'inet6', 'address': '::1', 'netmask': '128', 'scope': 'local'}],
                                'counters': {'bytes_received': 0, 'bytes_sent': 0, 'packets_received': 0, 'packets_sent': 0},
                                'hwaddr': '',
                                'host_name': '',
                                'mtu': 65536,
                                'state': 'up',
                                'type': 'loopback'}}}
        ```

    
    
* **Usage Example:**

```python
In [0]: data = {"container_pool": "server1",
               "operation":      "list_containers"}
In [1]: result = requests.get(BASE_URL + "container/", data).json()
In [2]: print(result)
Out[2]: {'containers': ['my-container']}
```

```python
In [0]: data = {"container_name": "my-container",
               "container_pool": "server1",
               "operation":      "information"}
In [1]: result = requests.get(BASE_URL + "container/", data).json()
In [2]: print(result)
Out[2]: {'disk': {},
         'memory': {'usage': 141582336, 'usage_peak': 141582336, 'swap_usage': 0, 'swap_usage_peak': 0},
         'network': {'eth0': {'addresses': [{'family': 'inet', 'address': '192.168.122.14', 'netmask': '24', 'scope': 'global'},
                                            {'family': 'inet6', 'address': 'fe80::216:3eff:feed:a5bf', 'netmask': '64', 'scope': 'link'}],
                             'counters': {'bytes_received': 9684, 'bytes_sent': 558, 'packets_received': 129, 'packets_sent': 7},
                             'hwaddr': '00:16:3e:ed:a5:bf',
                             'host_name': 'veth8WD1SA',
                             'mtu': 1500,
                             'state': 'up',
                             'type': 'broadcast'},
                     'lo': {'addresses': [{'family': 'inet', 'address': '127.0.0.1', 'netmask': '8', 'scope': 'local'},
                                          {'family': 'inet6', 'address': '::1', 'netmask': '128', 'scope': 'local'}],
                            'counters': {'bytes_received': 0, 'bytes_sent': 0, 'packets_received': 0, 'packets_sent': 0},
                            'hwaddr': '',
                            'host_name': '',
                            'mtu': 65536,
                            'state': 'up',
                            'type': 'loopback'}}}
```

##### Container: POST #####
* **Description:**
* **Required Parameters:**
    * ``"operation"``: Desired operation (``"start"``, ``"stop"``, ``"freeze"``,
    ``"unfreeze"``, ``"delete"``, ``"migrate"``, ``"create"``).
    * ``"container_name"``: Name of the container.
    * ``"container_pool"``: Name of the container pool.
* **Optional Parameters:**
    * ``"destination_pool"``: For migrations.
    * ``"image_type"``: To create containers, specify the image to be used.
* **Returns:**
    - SUCCESS: ``{'success': 'Operation successful'}``
    - WARNING:
    - ERROR: ``{'error': str(error Description)}``
* **Usage Example:**

This is the same for ``"start"``, ``"stop"``, ``"freeze"``, ``"unfreeze"`` and ``"delete"`` operations:

```python
In [0]: data = {"container_name": "my-container",
                "container_pool": "server1",
                "operation":      "start"}
In [1]: result = requests.post(BASE_URL + "container/", data).json()
In [2]: print(result)
Out[2]: {'success': 'Operation successful'}
```

For ``"create"`` operations:

```python
In [0]: data = data = {"container_name": "my-container",
                       "container_pool": "server1",
                       "operation":      "create",
                       "image_type":     "ubuntu"}
In [1]: result = requests.post(BASE_URL + "container/", data).json()
In [2]: print(result)
Out[2]: {'success': 'Container created successfully.'}
```

For ``"migrate"`` operations:

```python
In [0]: data = {"container_name":   "my-container",
                "container_pool":   "server1",
                "destination_pool": "server2",
                "operation":        "migrate"}
In [1]: result = requests.post(BASE_URL + "container/", data).json()
In [2]: print(result)
Out[2]: {'success': 'Container migrated successfully.'}
```

#### Image ####
##### Image: GET #####
* **Description:** Get the available Images to create containers.
* **Required Parameters:** -
* **Optional Parameters:**
    * ``"image_pool"``: List the images from a registered image pool
* **Returns:**
    - SUCCESS:``{'images': {'<IMG_ALIAS>': '<IMG_FINGERPRINT>'}, 'success': 'Operation successful'}``
    - WARNING: -
    - ERROR: ``{'error': str(error Description)}``
* **Usage Example:**

```python
In [0]: data = {"container_pool": container_pool,
                "operation":      "list_containers"}
In [1]: result = requests.get(BASE_URL + "image/", data).json()
In [2]: print(result)
Out[2]: {'images': {'ubuntu': '315bedd32580c3fb79fd2003746245b9fe6a8863fc9dd990c3a2dc90f4930039'},
         'success': 'Operation successful'}
```
