import json
import pkgutil
import subprocess
import simplejson
# Stacktrace stuff
import traceback

import colorama
import urllib3
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from pylxd import Client
from django.core import serializers
from datetime import *

from .models import Container, Pool, Image
from containers_site.COPA_general import *

# Disable SSL warnings on terminal
urllib3.disable_warnings()

# Enable colorama module for Stacktrace
colorama.init()


def load_modules_from_dir(dirname):
    for importer, package_name, _ in pkgutil.iter_modules([dirname]):
        full_package_name = "%s.%s" % (dirname, package_name)
        mdl = importer.find_module(package_name).load_module(full_package_name)
        return mdl


def alert_type(content):
    a_type = {"success": "alert-success",
              "error":   "alert-danger",
              "info":    "alert-info",
              "warning": "alert-warning"}
    return a_type[content]


def index(request):
    return redirect("welcome")


def welcome(request):
    template = loader.get_template("core/welcome.html")
    return HttpResponse(template.render({}, request))


def containers_list(request, message="", alert=""):
    containers = dict()
    template = loader.get_template("core/containers_list.html")
    servers = get_server_list()
    for server in servers:
        pk_server = Pool.objects.get(name=server)
        o_ip = get_ip_by_name(server)
        try:
            client_server = create_client(o_ip)
            containers[server] = dict()
            all_obj_server = Container.objects.filter(pool=pk_server)
            for o in all_obj_server:
                if o.full_network_info is not None:
                    o.full_network_info = json.loads(o.full_network_info)

            containers[
                server] = all_obj_server  # client_server.containers.all()
        except Exception as e:
            message += "<li>Error obtaining the containers list on server" \
                       " {}: {}</li>".format(o_ip, str(e))
            alert = alert_type("error")

            # Stacktrace
            colorama.Fore.RED + traceback.format_exc() + colorama.Fore.RESET

    params = {"containers": containers,
              "servers":    servers,
              "message":    message,
              "title":      "Containers",
              "alert_type": alert}
    return HttpResponse(template.render(params, request))


def containers_start(request, xhost, container_name):
    host = get_ip_by_name(xhost)
    try:
        client_server = create_client(host)
        container = client_server.containers.get(container_name)
        result = container.start(wait=True)
        cont_obj = Container.objects.get(name=container_name,
                                         pool=Pool.objects.get(name=xhost))
        cont_obj.status = container.status
        cont_obj.save()
        message = "Container started successful."
        alert = alert_type("success")
    except Exception as e:
        message = "Container error to start: " + str(e)
        alert = alert_type("error")

        # Stacktrace
        colorama.Fore.RED + traceback.format_exc() + colorama.Fore.RESET

    return containers_list(request, message, alert)


def containers_stop(request, xhost, container_name):
    host = get_ip_by_name(xhost)
    try:
        client_server = create_client(host)
        container = client_server.containers.get(container_name)
        result = container.stop(wait=True)
        cont_obj = Container.objects.get(name=container_name,
                                         pool=Pool.objects.get(name=xhost))
        cont_obj.status = container.status
        cont_obj.save()
        message = "Container stopped successful."
        alert = alert_type("success")
    except Exception as e:
        message = "Container error stop: " + str(e)
        alert = alert_type("error")

        # Stacktrace
        colorama.Fore.RED + traceback.format_exc() + colorama.Fore.RESET

    return containers_list(request, message, alert)


def containers_delete(request, xhost, container_name):
    host = get_ip_by_name(xhost)
    try:
        client_server = create_client(host)
        container = client_server.containers.get(container_name)
        result = container.delete(wait=True)
        Container.objects.get(pool=Pool.objects.get(name=xhost),
                              name=container_name).delete()
        message = "Container deleted successfully."
        alert = alert_type("success")
    except Exception as e:
        message = "Container error to delete: " + str(e)
        alert = alert_type("error")

        # Stacktrace
        colorama.Fore.RED + traceback.format_exc() + colorama.Fore.RESET

    return containers_list(request, message, alert)


def containers_freeze(request, xhost, container_name):
    host = get_ip_by_name(xhost)
    try:
        client_server = create_client(host)
        container = client_server.containers.get(container_name)
        result = container.freeze(wait=True)
        cont_obj = Container.objects.get(name=container_name,
                                         pool=Pool.objects.get(name=xhost))
        cont_obj.status = container.status
        cont_obj.save()
        message = "Container frozen successful."
        alert = alert_type("success")
    except Exception as e:
        message = "Container error to frozen: " + str(e)
        alert = alert_type("error")

        # Stacktrace
        colorama.Fore.RED + traceback.format_exc() + colorama.Fore.RESET

    return containers_list(request, message, alert)


def containers_new(request):
    servers = None
    images = None
    message = ""
    alert = ""
    try:
        servers = get_server_list()
    except Exception as e:
        message += "Error getting the server list: {}.".format(e)
        alert = alert_type("error")

    try:
        images = get_images_list()
    except Exception as e:
        message += "Error getting the images list: {}.".format(e)
        alert = alert_type("error")

    template = loader.get_template("core/new_container.html")
    params = {"servers":    servers,
              "images":     images,
              "message":    message,
              "alert_type": alert}
    return HttpResponse(template.render(params, request))


def containers_add(request):
    message = ""
    a_type = alert_type("success")
    container_name = str(request.POST.get("container_name"))
    xserver = str(request.POST.get("server"))
    image_type = str(request.POST.get("image_type"))
    profile = str(request.POST.get("profile"))
    wait_creation = bool(request.POST.get("wait_creation"))
    values = []
    config = {"name":   container_name,
              "source": {"server":      "https://" + IMAGE_HOST + ":8443",
                         "protocol":    "lxd",
                         "type":        "image",
                         "mode":        "pull",
                         "fingerprint": image_type}
              }
    server = get_ip_by_name(xserver)
    try:
        client_server = create_client(server)
        print("HERE!")
        container = client_server.containers.create(config, wait=wait_creation)
        print("HERE")
        container.start()
        message = "Container created sucessfully, go to admin container go " \
                  "to Containers list"
        Container(name=container_name,
                  pool=Pool.objects.get(name=xserver),
                  status=container.status).save()
    except Exception as e:
        message = "Container creation error: " + str(
                e) + " / " + server + " / " + xserver
        a_type = alert_type("error")

    servers = get_server_list()
    images = get_images_list()
    params = {"servers":    servers,
              "images":     images,
              "values":     values,
              "message":    message,
              "alert_type": a_type}
    template = loader.get_template("core/new_container.html")
    return HttpResponse(template.render(params, request))


def containers_migrate(request, origin, name_container, destination):
    ip_origin = get_ip_by_name(origin)
    ip_destination = get_ip_by_name(destination)
    try:
        client_origin = create_client(ip_origin)
        container = client_origin.containers.get(name_container)
        client_destination = create_client(ip_destination)
        container.migrate(client_destination, wait=True)
        container = client_origin.containers.get(name_container)
        container.delete(wait=True)
        cont_obj = Container.objects.get(name=name_container,
                                         pool=Pool.objects.get(name=origin))
        cont_obj.pool = Pool.objects.get(name=destination)
        cont_obj.save()
        message = "Container migration successful."
        alert = alert_type("success")
    except Exception as e:
        message = "Container migration error: " + str(e)
        alert = alert_type("error")

        # Stacktrace
        colorama.Fore.RED + traceback.format_exc() + colorama.Fore.RESET

    return containers_list(request, message, alert)


def containers_terminal(request, server, container_name):
    server_socket = request.get_host().replace(":" + request.get_port(), "")
    container_address = get_ip_by_name(server) + "/" + container_name
    template = loader.get_template("core/terminal.html")
    return HttpResponse(template.render({"container_address": container_address,
                                         "server_socket":     server_socket,
                                         "container_name":    container_name},
                                        request))


def containers_info(request, xhost, container_name):
    host = get_ip_by_name(xhost)
    template = loader.get_template("core/container_info.html")
    try:
        client_server = create_client(host)
        container = Container.objects.get(name=container_name, pool=xhost)
        if container.full_network_info is not None:
            container.full_network_info = json.loads(
                    container.full_network_info)
    except Exception as e:
        container = None
        message = "Error deleting container: " + str(e)
        alert = alert_type("error")

        # Stacktrace
        colorama.Fore.RED + traceback.format_exc() + colorama.Fore.RESET

    params = {"container": container,
              "title":     "Container information"}
    return HttpResponse(template.render(params, request))


def containers_unfreeze(request, xhost, container_name):
    a_type = alert_type("success")
    host = get_ip_by_name(xhost)
    try:
        client_server = create_client(host)
        container = client_server.containers.get(container_name)
        result = container.unfreeze(wait=True)
        cont_obj = Container.objects.get(name=container_name,
                                         pool=Pool.objects.get(name=xhost))
        cont_obj.status = container.status
        cont_obj.save()
        message = "Container unfreeze successful"
    except Exception as e:
        message = "Container error unfreeze: " + str(e)
        a_type = alert_type("error")

    return containers_list(request, message, a_type)


@csrf_exempt
def api_execution(request):
    response = {}
    code = -1
    result = None
    try:
        ostring = request.body
        js = json.loads(ostring)

        oper = js["operation"]

        if oper == "copa_host_command":
            command = js["cmd"]
            if not isinstance(command, list):
                raise Exception("Parameter 'cmd' must be a list")
            result = subprocess.check_output(command)

        elif oper == "copa_module_execution":
            pycom = js["method"]
            args = js["args"]
            if pycom == "":
                raise Exception("Error: You must select the procedure/function "
                                "to be called!")
            load_modules_from_dir(COPA_HOME + "/containers_site/core/"
                                              "copa_modules/")
            exec("result = modules." + pycom + "( " + args + ") ")

        else:
            x_server = get_ip_by_name(js["container_pool"])
            server = create_client(x_server)

            if oper not in ["create", "images_list"]:
                x_container = js["container_name"]
                db_container = Container.objects.get(name=x_container,
                                                     pool=x_server)
                container = server.containers.get(x_container)

                if oper == "start":
                    container.start(wait=True)
                    db_container.status = container.status
                    db_container.save()
                    message = "Container created successfully."

                elif oper == "stop":
                    container.stop(wait=True)
                    db_container.status = container.status
                    db_container.save()
                    message = "Container stopped successfully."

                elif oper == "freeze":
                    container.freeze(wait=True)
                    db_container.status = container.status
                    db_container.save()
                    message = "Container frozen successfully."

                elif oper == 'unfreeze':
                    container.unfreeze(wait=True)
                    db_container.status = container.status
                    db_container.save()
                    message = "Container unfrozen successfully"

                elif oper == "delete":
                    container.delete(wait=True)
                    db_container.status = container.status
                    db_container.save()
                    message = "Container deleted successfully."

                elif oper == "migrate":
                    ip_destination = get_ip_by_name(js["destination_pool"])
                    client_destination = create_client(ip_destination)
                    container.migrate(client_destination, wait=True)
                    message = "Container migration successful."
                    container = server.containers.get(x_container)
                    container.delete(wait=True)
                    db_container.pool = Pool.objects.get(
                            name=js["destination_pool"])
                    db_container.status = container.status
                    db_container.save()

                elif oper == "information":
                    infos = container.state()
                    result = dict()
                    result["cpu"] = infos.cpu  # just available in lxd >= 2.19
                    result["disk"] = infos.disk
                    result["memory"] = infos.memory
                    result["network"] = infos.network

                elif oper == "command_execution":
                    command = js["cmd"]
                    if not isinstance(command, list):
                        raise Exception("Parameter 'cmd' must be a list")
                    result = container.execute(command)

            elif oper == "create":
                container_name = js["container_name"]
                container_pool = get_ip_by_name(js["container_pool"])
                image_type = js["image_type"]
                values = []
                config = {"name":   container_name,
                          "source": {
                              "server":      "https://" + IMAGE_HOST + ":8443",
                              "protocol":    "",
                              "type":        "image",
                              "mode":        "pull",
                              "fingerprint": image_type}}
                client_server = create_client(container_pool)

                container = client_server.containers.create(config, wait=True)
                Container(name=container_name,
                          pool=Pool.objects.get(name=container_pool),
                          status=container.status).save()
                message = "Container created successfully"

            elif oper == "images_list":
                result = get_images_list()

            else:
                raise Exception("Unknown operation")

        code = 0
        message = "Process successful"
    except Exception as e:
        message = "COPA API error: " + str(e)

    response["code"] = code
    response["message"] = message
    response["result"] = result

    return JsonResponse(response, safe=False)
