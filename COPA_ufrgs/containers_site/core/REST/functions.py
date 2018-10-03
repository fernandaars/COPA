from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from containers_site.COPA_general import IMAGE_HOST, create_client
from ..models import Container, Pool, Image


class RestFunctions(object):
    @staticmethod
    def check_required_fields(required_fields=None, provided_fields=None):
        for requirement in required_fields:
            if requirement not in provided_fields:
                raise Exception("Required Field '{}' not in"
                                " post".format(requirement))

    @staticmethod
    @csrf_exempt
    def pool(request):
        """
        """
        response = dict()
        if request.method == "GET":
            response["pools"] = list(
                    Pool.objects.all().values_list("name", "local_ip", ))
            response["success"] = "pools"

        elif request.method == "POST":
            try:
                required_fields = ["operation"]
                RestFunctions.check_required_fields(required_fields,
                                                    request.POST)
            except Exception as e:
                return JsonResponse({"error": str(e)})

            if request.POST["operation"] == "add":
                try:
                    required_fields = ["container_pool", "ip"]
                    RestFunctions.check_required_fields(required_fields,
                                                        request.POST)
                    Pool(name=request.POST["container_pool"],
                         local_ip=request.POST["ip"]).save()

                    response["container_pool"] = request.POST["container_pool"]
                    response["local_ip"] = request.POST["ip"]
                    response["success"] = "Container pool added Successfully"
                except Exception as e:
                    return JsonResponse({"error": str(e)})

            elif request.POST["operation"] == "remove":
                try:
                    required_fields = ["container_pool"]
                    RestFunctions.check_required_fields(required_fields,
                                                        request.POST)
                    Pool.objects.get(
                            name=request.POST["container_pool"]).delete()

                    response["container_pool"] = request.POST["container_pool"]
                    response["success"] = "Container pool removed successfully."
                except Exception as e:
                    return JsonResponse({"error": str(e)})

        else:
            response["error"] = "Method not allowed"

        return JsonResponse(response)

    @staticmethod
    @csrf_exempt
    def container(request):
        """
        """
        response = dict()
        if request.method == "GET":
            try:
                required_fields = ["operation",
                                   "container_pool"]
                RestFunctions.check_required_fields(required_fields,
                                                    request.GET)
                pool_obj = Pool.objects.get(name=request.GET["container_pool"])
                server = create_client(pool_obj.local_ip + ":8443")
            except Exception as e:
                return JsonResponse({"error": str(e)})

            if request.GET["operation"] == "information":
                try:
                    required_fields = ["container_name"]
                    RestFunctions.check_required_fields(required_fields,
                                                        request.GET)

                    container_obj = Container.objects.get(
                            name=request.GET["container_name"],
                            pool=request.GET["container_pool"])
                    container = server.containers.get(container_obj.name)

                    info = container.state()
                    # TODO: How is this implemented?
                    try:
                        response["cpu"] = info.cpu
                    except Exception as e:
                        response["warning"] = str(e)
                    response["disk"] = info.disk
                    response["memory"] = info.memory
                    response["network"] = info.network
                except Exception as e:
                    response["error"] = str(e)

            elif request.GET["operation"] == "list_containers":
                response["containers"] = []
                for container in server.containers.all():
                    response["containers"].append(container.name)

        elif request.method == "POST":
            try:
                required_fields = ["container_name", "operation",
                                   "container_pool"]
                RestFunctions.check_required_fields(required_fields,
                                                    request.POST)

                server = create_client(Pool.objects.get(
                    name=request.POST["container_pool"]).local_ip + ":8443")

                container = None
                if request.POST["operation"] != "create":
                    container_obj = Container.objects.get(
                            name=request.POST["container_name"],
                            pool=request.POST["container_pool"])
                    container = server.containers.get(container_obj.name)

                if request.POST["operation"] == "start":
                    try:
                        container.start(wait=True)
                        container_obj.status = container.status
                        container_obj.save()
                        response["success"] = "Operation successful"
                    except Exception as e:
                        response["error"] = str(e)

                elif request.POST["operation"] == "stop":
                    try:
                        container.stop(wait=True)
                        container_obj.status = container.status
                        container_obj.save()
                        response["success"] = "Operation successful"
                    except Exception as e:
                        response["error"] = str(e)

                elif request.POST["operation"] == "freeze":
                    try:
                        container.freeze(wait=True)
                        container_obj.status = container.status
                        container_obj.save()
                        response["success"] = "Operation successful"
                    except Exception as e:
                        response["error"] = str(e)

                elif request.POST["operation"] == "unfreeze":
                    try:
                        container.unfreeze(wait=True)
                        container_obj.status = container.status
                        container_obj.save()
                        response["success"] = "Operation successful"
                    except Exception as e:
                        response["error"] = str(e)

                elif request.POST["operation"] == "delete":
                    try:
                        container.delete(wait=True)
                        container_obj.delete()
                        response["success"] = "Operation successful"
                    except Exception as e:
                        response["error"] = str(e)

                elif request.POST["operation"] == "migrate":
                    try:
                        required_fields = ["destination_pool"]
                        RestFunctions.check_required_fields(required_fields,
                                                            request.POST)
                        dest_pool_obj = Pool.objects.get(
                                name=request.POST["destination_pool"])

                        destination_pool = create_client(
                                dest_pool_obj.local_ip + ":8443")

                        container.migrate(destination_pool, wait=True)
                        container_obj.pool = dest_pool_obj
                        container_obj.save()
                        response["success"] = "Container migrated successfully."
                        try:
                            container_orig = server.containers.get(
                                    container_obj.name)
                            container_orig.delete(wait=True)
                        except Exception as e:
                            response["warning"] = str(e)

                    except Exception as e:
                        response["error"] = str(e)

                elif request.POST["operation"] == "create":
                    try:
                        required_fields = ["image_type"]
                        RestFunctions.check_required_fields(required_fields,
                                                            request.POST)
                        im = Image.objects.get(alias=request.POST["image_type"])
                        config = {"name": request.POST["container_name"],
                                  "source": {"server":      "https://"
                                                            + IMAGE_HOST
                                                            + ":8443",
                                             "protocol":    "",
                                             "type":        "image",
                                             "mode":        "pull",
                                             "fingerprint": im.fingerprint}}

                        c = server.containers.create(config, wait=True)
                        c.start()
                        Container(name=c.name, status=c.status,
                                  pool=Pool.objects.get(name=request.POST["container_pool"])).save()
                        response["success"] = "Container created successfully."

                    except Exception as e:
                        response["error"] = str(e)

                else:
                    response["error"] = "Operation '" \
                                        + request.POST["operation"] \
                                        + "' invalid"
            except Exception as e:
                return JsonResponse({"error": str(e)})

        else:
            response["error"] = "Method not allowed"

        return JsonResponse(response)

    @staticmethod
    @csrf_exempt
    def image(request):
        """
        """
        response = dict()
        if request.method == "GET":
            try:
                required_fields = []
                RestFunctions.check_required_fields(required_fields,
                                                    request.GET)
            except Exception as e:
                response["error"] = str(e)

            if "image_pool" in request.GET:
                image_pool = request.GET["image_pool"]
            else:
                image_pool = IMAGE_HOST

            images = dict()
            aliases = []
            cp_c = 0

            try:
                client = create_client(image_pool + ":8443")
                all_images = client.images.all()
                for i in all_images:
                    if len(i.aliases) > 0 and i.fingerprint is not None:
                        for item in i.aliases:
                            aliases.append(item["name"])
                        images[aliases[cp_c]] = i.fingerprint
                        cp_c = cp_c + 1

                response["images"] = images
                response["success"] = "Operation successful"
            except Exception as e:
                response["error"] = str(e)

        elif request.method == "POST":
            pass

        else:
            response["error"] = "Method not allowed"

        return JsonResponse(response)
