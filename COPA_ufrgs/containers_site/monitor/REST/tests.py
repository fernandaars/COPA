import random

import requests

BASE_URL = "http://localhost:8000/REST/network/"

BASE_LOCUS = ["server1", "server2"]


def test_request_locus_all():
    data = dict()

    print(requests.get(BASE_URL + "locus/", data).json())


def test_get_kpilink(show=False, locus=None, last=None):
    data = {"locus": locus,
            "last":  last}

    cmd_measures_request = requests.get(BASE_URL + "kpilink/", data).json()

    if "success" in cmd_measures_request:
        print("Success: " + cmd_measures_request["success"])
    else:
        print(cmd_measures_request)
    if show:
        for m in cmd_measures_request["measurements"]:
            print(m)


def test_get_kpicommand(show=False, locus=None, last=None):
    data = {"locus": locus,
            "last":  last}

    kpi_measures_request = requests.get(BASE_URL + "kpicommand/", data).json()

    if "success" in kpi_measures_request:
        print("Success: " + kpi_measures_request["success"])
    else:
        print(kpi_measures_request)
    if show:
        for m in kpi_measures_request["measurements"]:
            print(m)


def test_get_kpiresource(show=False, locus=None, last=None):
    data = {"locus": locus,
            "last":  last}

    kpiresource_request = requests.get(BASE_URL + "kpiresource/", data).json()

    if "success" in kpiresource_request:
        print("Success: " + kpiresource_request["success"])
    else:
        print(kpiresource_request)
    if show:
        for m in kpiresource_request["measurements"]:
            print(m)


def test_get_kpiwireless(show=False, locus=None, last=None):
    data = {"locus": locus,
            "last":  last}

    kpiwireless_request = requests.get(BASE_URL + "kpiwireless/", data).json()

    if "success" in kpiwireless_request:
        print("Success: " + kpiwireless_request["success"])
    else:
        print(kpiwireless_request)
    if show:
        for m in kpiwireless_request["measurements"]:
            print(m)


def test_post_configuration(delegation_mode=None, auto_delegation_type=None):
    data = dict()
    if delegation_mode:
        data["delegation_mode"] = delegation_mode
    if auto_delegation_type:
        data["auto_delegation_type"] = auto_delegation_type

    print(requests.post(BASE_URL + "configuration/", data).json())


def test_post_kpilink(data=None):
    if not data:
        data = {"locus1":              BASE_LOCUS[0],
                "locus2":              BASE_LOCUS[1],
                "jitter_1to2":         random.randrange(0, 100, True),
                "latency_max_1to2":    random.randrange(0, 100, True),
                "latency_median_1to2": random.randrange(0, 100, True),
                "latency_min_1to2":    random.randrange(0, 100, True),
                "jitter_2to1":         random.randrange(0, 100, True),
                "latency_max_2to1":    random.randrange(0, 100, True),
                "latency_median_2to1": random.randrange(0, 100, True),
                "latency_min_2to1":    random.randrange(0, 100, True),
                "throughput":          random.randrange(0, 100, True)}

    print(requests.post(BASE_URL + "kpilink/", data).json())


def test_post_kpicommand(data=None):
    if not data:
        data = {"locus":           BASE_LOCUS[0],
                "proc_time":       random.randrange(0, 100, True),
                "response_time":   random.randrange(0, 100, True),
                "cmd":             "",
                "cmd_type":        ""}

    print(requests.post(BASE_URL + "kpicommand/", data).json())


def test_post_kpiresource(data=None):
    if not data:
        data = {"locus": BASE_LOCUS[0],
                "CPU":             random.randrange(0, 1000, True),
                "memory":          random.randrange(0, 1000, True)}

    print(requests.post(BASE_URL + "kpiresource/", data).json())


def test_post_kpiwireless(data=None):
    if not data:
        data = {"locus":               BASE_LOCUS[0],
                "mac":                 "",
                "mfb":                 True,
                "tdls":                True,
                "wmm":                 True,
                "authenticated":       True,
                "authorized":          True,
                "expected_throughput": "",
                "inactive_time":       "",
                "preamble":            "",
                "rx_bitrate":          "",
                "rx_bytes":            0,
                "rx_packets":          0,
                "signal":              "",
                "signal_avg":          "",
                "tx_bitrate":          "",
                "tx_bytes":            0,
                "tx_failed":           0,
                "tx_retries":          0}

    print(requests.post(BASE_URL + "kpiwireless/", data).json())


if __name__ == "__main__":
    print("POST TESTS!")
    for i in range(0, 10):
        test_post_kpilink()
        test_post_kpicommand()
        test_post_kpiresource()
        test_post_kpiwireless()
        test_post_configuration()

    print("REQUEST TESTS!")
    test_request_locus_all()
    test_get_kpilink(locus=BASE_LOCUS[0])
    test_get_kpicommand(locus=BASE_LOCUS[0])
    test_get_kpiresource(locus=BASE_LOCUS[0])
    test_get_kpiwireless(locus=BASE_LOCUS[0])

    pass
