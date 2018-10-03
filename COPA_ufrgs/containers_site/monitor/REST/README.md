# COPA Monitor REST API #

This documentation describes the REST functions available for use
with the COPA Monitor application and also demonstrates how to do so
using the Pyhton Requests library.

## Available functions ##

|             Function            |           URI          |            Method           |
|:--------------------------------|:-----------------------|:---------------------------:|
| [Locus List](#locus)            | /network/locus         |  [GET](#locus-get)          |
| [KPI Link](#kpi-link)           | /network/kplink        |  [GET](#kpi-link-get)       |
|                                 |                        |  [POST](#kpi-link-post)      |
| [KPI Command](#kpi-command)     | /network/kpcommand     |  [GET](#kpi-command-get)    |
|                                 |                        |  [POST](#kpi-command-post)   |
| [KPI Resource](#kpi-resource)   | /network/kpiresource   |  [GET](#kpi-resource-get)   |
|                                 |                        |  [POST](#kpi-resource-post)  |
| [KPI Wireless](#kpi-wireless)   | /network/kpiwireless   |  [GET](#kpi-wireless-get)   |
|                                 |                        |  [POST](#kpi-wireless-post)  |
| [Configuration](#configuration) | /network/configuration |  [POST](#configuration-post) |

#### Locus ####
##### Locus: GET #####
* **Description:** Returns a list of all existing Locus in the experiment.
* **Required Parameters:** -
* **Optional Parameters:** -
* **Returns:**
    - SUCCESS: ``{'locus': \[LOCUS_LIST\], 'success': 'request_locus_all'}``
        + The LOCUS_LIST will be a list of strings.
            * `'locus'` (List): List of strings containing the names of the available Locus
    - ERROR: ``{'error': 'ERROR DESCRIPTION'}``
* **Usage Example:**

```python
In [1]: import requests
In [2]: data = {}
In [3]: response = requests.get(BASE_URL + 'locus_all/', data).json()
Out[3]: {'locus': ['Tier1', 'Tier2'], 'success': 'request_locus_all'}
```

#### KPI Link ####
##### KPI Link: GET #####
* **Description:** Returns a list of all measured Link KPIS.
                   (Specify the `'last'` parameter to limit the number of measurements returned)
* **Required Parameters:**
    - `'locus'` (Str): Name of the locus to request the measurements.
* **Optional Parameters:**
    - `'last'` (Int): Number of measurements requested (last *N* measurements)
* **Returns:**
    - SUCCESS: ``{'measurements':\[MEASUREMENTS_LIST\], 'success': 'request_kpilink'}``
        + The MEASUREMENTS_LIST will be a list of dictionaries, each containing:
            * `'id'` (Int): Measurement ID number
            * `'locus1_id'` (Int): Locus ID number
            * `'locus2_id'` (Int): Locus2 ID number
            * `'jitter_1to2'` (TYPE):
            * `'latency_max_1to2'` (TYPE):
            * `'latency_median_1to2'` (TYPE):
            * `'latency_min_1to2'` (TYPE):
            * `'jitter_2to1'` (TYPE):
            * `'latency_max_2to1'` (TYPE):
            * `'latency_median_2to1'` (TYPE):
            * `'latency_min_2to1'` (TYPE):
            * `'throughput'` (TYPE): Link Throughput
            * `'timestamp'` (Datetime):
    - ERROR: ``{'error': 'ERROR DESCRIPTION'}``
* **Usage Example:**

```python
In [1]: import requests
In [2]: data = {'locus':'Locus1', 'last':''}
In [3]: request = requests.get(BASE_URL + 'kpilink/', data).json()
Out[3]: {'measurements': [{'id': 1,
                           'locus1_id': 1,
                           'locus2_id': 2,
                           'jitter_1to2': 77.0,
                           'latency_max_1to2': 29.0,
                           'latency_median_1to2': 98.0,
                           'latency_min_1to2': 24.0,
                           'jitter_2to1': 87.0,
                           'latency_max_2to1': 49.0,
                           'latency_median_2to1': 97.0,
                           'latency_min_2to1': 52.0,
                           'throughput': 37.0,
                           'timestamp': '2017-11-18T03:21:11.106Z'}],
         'success': 'request_kpilink'}

```

##### KPI Link: POST #####
* **Description:** Post Link KPIs measurements.
* **Required Parameters:**
    - `'locus1'` (Str): Name of the locus
    - `'locus2'` (Str): Name of the second locus
    - `'jitter_1to2'` (TYPE):
    - `'latency_max_1to2'` (TYPE):
    - `'latency_median_1to2'` (TYPE):
    - `'latency_min_1to2'` (TYPE):
    - `'jitter_2to1'` (TYPE):
    - `'latency_max_2to1'` (TYPE):
    - `'latency_median_2to1'` (TYPE):
    - `'latency_min_2to1'` (TYPE):
    - `'throughput'` (TYPE): Link Throughput
* **Optional Parameters:** -
* **Returns:**
    - SUCCESS: ``{'success': 'post_kpilink'}``
    - ERROR: ``{'error': 'ERROR DESCRIPTION'}``
* **Usage Example:**

```python
In [1]: import requests
In [2]: data = {'locus1': 'Locus1',
                'locus2': 'Locus2',
                'jitter_1to2': 77.0,
                'latency_max_1to2': 29.0,
                'latency_median_1to2': 98.0,
                'latency_min_1to2': 24.0,
                'jitter_2to1': 87.0,
                'latency_max_2to1': 49.0,
                'latency_median_2to1': 97.0,
                'latency_min_2to1': 52.0,
                'throughput': 37.0}
In [3]: request = requests.get(BASE_URL + 'post_kpilink/', data).json()
Out[3]: {'success': 'post_kpilink'}

```

#### KPI Command ####
#### KPI Command: GET ####
* **Description:** Returns a list of all commands issued by the user, along with the respective KPIs.
                   (Specify the `'last'` parameter to limit the number of measurements returned)
* **Required Parameters:**
    - `'locus'` (Str): Name of the locus to request the measurements.
* **Optional Parameters:**
    - `'last'` (Int): Number of measurements requested (last *N* measurements)
* **Returns:**
    - SUCCESS: ``{'measurements':\[MEASUREMENTS_LIST\], 'success': 'request_kpicommand'}``
        + The MEASUREMENTS_LIST will be a list of dictionaries, each containing:
            * `'id'` (Int): Measurement ID number
            * `'locus_id'` (Int): Locus ID number
            * `'proc_time'` (Float): Processing time (ms)
            * `'response_time'` (Float): Response time (ms)
            * `'cmd'` (Str): Command issued
            * `'cmd_type'` (Str): Command type (v - Voice; g - Gesture)
            * `'timestamp'` (Datetime):
    - ERROR: ``{'error': 'ERROR DESCRIPTION'}``
* **Usage Example:**

```python
In [1]: import requests
In [2]: data = {'locus':'Locus1'}
In [3]: request = requests.get(BASE_URL + 'kpicommand/', data).json()
Out[3]: {'measurements': [{'id': 1,
                           'locus_id': 1,
                           'proc_time': 66.0,
                           'response_time': 22.0,
                           'cmd': '',
                           'cmd_type': '',
                           'timestamp': '2017-11-18T19:28:54.249Z'}],
         'success': 'request_kpicommand'}
```

##### KPI Command: POST #####
* **Description:** Post command relative KPIs.
* **Required Parameters:**
    - `'locus'` (Str): Name of the locus to request the measurements.
    - `'proc_time'` (Float): Processing time (ms)
    - `'response_time'` (Float): Response time (ms)
    - `'cmd'` (Str): Command issued
    - `'cmd_type'` (Str): Command type (v - Voice; g - Gesture)
* **Optional Parameters:** -
* **Returns:**
    - SUCCESS: ``{'success': 'post_kpicommand'}``
    - ERROR: ``{'error': 'ERROR DESCRIPTION'}``
* **Usage Example:**

```python
In [1]: import requests
In [2]: data = {'locus':'Locus1'
                'proc_time': 66.0,
                'response_time': 22.0,
                'cmd': '',
                'cmd_type': ''}
In [3]: request = requests.get(BASE_URL + 'kpicommand/', data).json()
Out[3]: {'success': 'post_kpicommand'}
```

#### KPI Resource ####
##### KPI Resource: GET #####
* **Description:** Return a list of all measured Locus Resources KPIs.
                   (Specify the `'last'` parameter to limit the number of measurements returned)
* **Required Parameters:**
    - `'locus'` (Str): Name of the locus to request the measurements.
* **Optional Parameters:**
    - `'last'` (Int): Number of measurements requested (last *N* measurements)
* **Returns:**
    - SUCCESS: ``{'measurements':\[MEASUREMENTS_LIST\], 'success': 'request_kpiresource'}``
        + The MEASUREMENTS_LIST will be a list of dictionaries, each containing:
            * `'id'` (Int): Measurement ID number
            * `'locus_id'` (Int): Locus ID number
            * `'CPU'` (Int): Percentage of CPU Load
            * `'memory'` (Int): Current memory usage
            * `'timestamp'` (Datetime):
    - ERROR: ``{'error': 'ERROR DESCRIPTION'}``
* **Usage Example:**

```python
In [1]: import requests
In [2]: data = {'locus':'Locus1'}
In [3]: request = requests.get(BASE_URL + 'kpiresource/', data).json()
Out[3]: {'measurements': [{'id': 1,
                           'locus_id': 1,
                           'CPU': 194.0,
                           'memory': 447.0,
                           'timestamp': '2017-11-18T19:32:40.511Z'}],
         'success': 'request_kpiresource'}
```

##### KPI Resource: POST #####
* **Description:** POST Locus Resources KPIs measurements.
* **Required Parameters:**
    - `'locus'` (Str): Name of the locus to request the measurements.
    - `'CPU'` (Int): Percentage of CPU Load
    - `'memory'` (Int): Current memory usage
* **Optional Parameters:** -
* **Returns:**
    - SUCCESS: ``{'success': 'post_kpiresource'}``
    - ERROR: ``{'error': 'ERROR DESCRIPTION'}``
* **Usage Example:**

```python
In [1]: import requests
In [2]: data = {'locus':'Locus1'
                'CPU': 194.0,
                'memory': 447.0}
In [3]: request = requests.post(BASE_URL + 'post_kpiresource/', data).json()
Out[3]: {'success': 'post_kpiresource'}
```

#### KPI Wireless ####
##### KPI Wireless: GET #####
* **Description:** Returns a list of all measured Wireless KPIs.
                   (Specify the `'last'` parameter to limit the number of measurements returned)
* **Required Parameters:**
    - `'locus'` (Str): Name of the locus to request the measurements.
* **Optional Parameters:**
    - `'last'` (Int): Number of measurements requested (last *N* measurements)
* **Returns:**
    - SUCCESS: ``{'measurements':\[MEASUREMENTS_LIST\], 'success': 'request_kpiwireless'}``
        + The MEASUREMENTS_LIST will be a list of dictionaries, each containing:
            * `'id'` (Int): Measurement ID number
            * `'locus_id'` (Int): Locus ID number
            * `'mac'` (Str): MAC Address of the Network card
            * `'mfb'` (Boolean):
            * `'tdls'` (Boolean):
            * `'wmm'` (Boolean):
            * `'authenticated'` (Boolean):
            * `'authorized'` (Boolean):
            * `'expected_throughput'` (TYPE):
            * `'inactive_time'` (TYPE):
            * `'preamble'` (TYPE):
            * `'rx_bitrate'` (TYPE):
            * `'rx_bytes'` (Int):
            * `'rx_packets'` (Int):
            * `'signal'` (TYPE):
            * `'signal_avg'` (TYPE):
            * `'tx_bitrate'` (TYPE):
            * `'tx_bytes'` (Int):
            * `'tx_failed'` (Int):
            * `'tx_retries'` (Int):
            * `'timestamp'` (Datetime):
    - ERROR: ``{'error': 'ERROR DESCRIPTION'}``
* **Usage Example:**

```python
In [1]: import requests
In [2]: data = {'locus':'Locus1'}
In [3]: request = requests.get(BASE_URL + 'kpiwireless/', data).json()
Out[3]: {'measurements': [{'id': 1,
                           'locus_id': 1,
                           'mac': '',
                           'mfb': True,
                           'tdls': True,
                           'wmm': True,
                           'authenticated': True,
                           'authorized': True,
                           'expected_throughput': '',
                           'inactive_time': '',
                           'preamble': '',
                           'rx_bitrate': '',
                           'rx_bytes': 0,
                           'rx_packets': 0,
                           'signal': '',
                           'signal_avg': '',
                           'tx_bitrate': '',
                           'tx_bytes': 0,
                           'tx_failed': 0,
                           'tx_retries': 0,
                           'timestamp': '2017-11-18T19:35:03.878Z'}],
         'success': 'request_kpiwireless'}
```

##### KPI Wireless: POST #####
* **Description:** POST Wireless KPIs measurements.
* **Required Parameters:**
    - `'locus'` (Str): Name of the locus to request the measurements.
    - `'mac'` (Str): MAC Address of the Network card
    - `'mfb'` (Boolean):
    - `'tdls'` (Boolean):
    - `'wmm'` (Boolean):
    - `'authenticated'` (Boolean):
    - `'authorized'` (Boolean):
    - `'expected_throughput'` (TYPE):
    - `'inactive_time'` (TYPE):
    - `'preamble'` (TYPE):
    - `'rx_bitrate'` (TYPE):
    - `'rx_bytes'` (Int):
    - `'rx_packets'` (Int):
    - `'signal'` (TYPE):
    - `'signal_avg'` (TYPE):
    - `'tx_bitrate'` (TYPE):
    - `'tx_bytes'` (Int):
    - `'tx_failed'` (Int):
    - `'tx_retries'` (Int):
* **Optional Parameters:** -
* **Returns:**
    - SUCCESS: ``{'success': 'post_kpiwireless'}``
    - ERROR: ``{'error': 'ERROR DESCRIPTION'}``
* **Usage Example:**

```python
In [1]: import requests
In [2]: data = {'locus': ,
                'mac': '',
                'mfb': True,
                'tdls': True,
                'wmm': True,
                'authenticated': True,
                'authorized': True,
                'expected_throughput': '',
                'inactive_time': '',
                'preamble': '',
                'rx_bitrate': '',
                'rx_bytes': 0,
                'rx_packets': 0,
                'signal': '',
                'signal_avg': '',
                'tx_bitrate': '',
                'tx_bytes': 0,
                'tx_failed': 0,
                'tx_retries': 0}
In [3]: request = requests.POST(BASE_URL + 'post_kpiwireless/', data).json()
Out[3]: {'success': 'post_kpiwireless'}
```

#### Configuration ####
##### Configuration: POST #####
* **Description:** Update the experiment's configurations.
* **Required Parameters:** -
* **Optional Parameters:**
    - `'delegation_mode'` (Str): Processing delegation mode ('m' - Manual; 'a' - Automatic)
    - `'auto_delegation_type'` (Str): Automatic delegation algorithm. Depends on availability.
* **Returns:**
    - SUCCESS: ``{'success': 'update_configuration'}``
    - ERROR: ``{'error': 'ERROR DESCRIPTION'}``
* **Usage Example:**

```python
In [1]: import requests
In [2]: data = {'delegation_mode': 'm',
                'auto_delegation_type': ''}
In [3]: request = requests.POST(BASE_URL + 'update_configuration/', data).json()
Out[3]: {'success': 'update_configuration'}
```
