from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from core.models import Configuration, Pool, Container
from ..models import KPICommand, KPILink, KPIResources, KPIWireless

from datetime import datetime, timedelta
from django.db.models import Avg, Q, F, Max

import json

class RestFunctions(object):
    @staticmethod
    def check_required_fields(required_fields=None, provided_fields=None):
        for requirement in required_fields:
            if requirement not in provided_fields:
                raise Exception("Required Field '{}' not in"
                                " post".format(requirement))

    @staticmethod
    def locus(request):
        """Request list of Tiers from an Configuration.
        """
        response = dict()
        if request.method == "GET":
            response["locus"] = list(
                    Pool.objects.all().values_list("name", flat=True))
            response["success"] = "locus"

        else:
            response["error"] = "Method not allowed"

        return JsonResponse(response)

    @staticmethod
    @csrf_exempt
    def dashboard(request):
        """KPI measurements.
        """
        response = dict()

        if request.method == "GET":

            try:
                pools = list(Pool.objects.all().values())

                response["data"] = list()
                # return JsonResponse(response)
            except ObjectDoesNotExist:
                return JsonResponse({"error": "Pool not registered"})

            try:
                time_threshold = datetime.now() - timedelta(seconds=30)
                for pool in pools:
                    resources = KPIResources.objects \
                        .filter(locus=pool["name"], timestamp__gt=time_threshold) \
                        .aggregate(cpu=Avg("CPU"),mem=Avg("memory"))

                    containers = list(Container.objects \
                        .filter(pool=pool["name"]) \
                        .values("name", "status"))

                    throughput = KPILink.objects \
                        .filter(locus1=pool["name"], timestamp__gt=time_threshold) \
                        .aggregate(throughput=Avg("throughput"))

                    if throughput["throughput"]:
                        throughput["throughput"] = float(throughput["throughput"])*1024

                    response["data"].append({
                        "name": pool["name"],
                        "cpu": resources["cpu"],
                        "mem": resources["mem"],
                        "throughput": throughput["throughput"],
                        "containers": containers
                    })

            except Exception as e:
                return JsonResponse({"error": str(e)})

            response["success"] = "dashboard"

        else:
            response["error"] = "Method not allowed"

        return JsonResponse(response)

    @staticmethod
    @csrf_exempt
    def dashboardlinks(request):#uma solicitação do cliente
        """KPI measurements.
        """
        response = dict() #variavel response inicializada como um dicionario vazio
        if request.method == "GET":#faz um pedido por meio de um metodo GET que pega as informações necessarias do banco de dados por http (a lista/JSON)

            try:
                required_fields = ["locus"]#"locus" é um required field
                RestFunctions.check_required_fields(required_fields,#verifica se existe "locus" no JSON enviado pelo servidor 
                                                    request.GET)
            except Exception as e:
                return JsonResponse({"error": str(e)})#se não tiver locus, retorna erro

            try:
                locus = Pool.objects.get(name=request.GET["locus"])#busca o objeto locus com o nome igual ao locus recebido 
                #locus = Pool.objects.get(name="Server1")
            except ObjectDoesNotExist:
                return JsonResponse({"error": "Pool not registered"})#se não tiver objeto com o mesmo nome, retorna erro

            try:
                temp = dict()#variavel temp inicializada como um dicionario vazio
                time_threshold = datetime.now() - timedelta(minutes=5)#estabelece um intervalo de dois minutos
                wireless_time_threshold = datetime.now() - timedelta(seconds=30)
                id_last_item = request.GET["id_last_item"]#recebe o ultimo id da lista dos dados que foi mandada
                
                data = list( #data recebe uma lista
                        KPILink.objects.filter((Q(locus1=locus) | Q(locus2=locus)), timestamp__gt=time_threshold, id__gt=id_last_item)#consulta o banco de dados de 2 em 2 min filtrando para valores maiores do que o id do ultimo item
                        # KPILink.objects.filter((Q(locus1=locus) | Q(locus2=locus)), timestamp__gt=time_threshold) 
                        .order_by("-timestamp")#ordena os dados por timestamp
                        .values()) #This method returns a list of all the values available in a given dictionary

                id_array = list()  

                for item in data:

                    id_array.append(item["id"]);
                    

                    if item["locus1_id"] == locus.name: #se achar o nome do locus 1
                        if not (item["locus2_id"] in temp):#se não achar o id do locus 2
                            temp[item["locus2_id"]] = {
                                "name": item["locus2_id"],
                                "jitter_down": [item["jitter_2to1"]],
                                "jitter_up": [item["jitter_1to2"]],
                                "latency_down": [item["latency_median_2to1"]],
                                "latency_up": [item["latency_median_1to2"]]
                            }
                        else:#se o id do locus 2 ja estiver na lista, apenas insere novos valores a ela
                            temp[item["locus2_id"]]["jitter_down"].insert(0, item["jitter_2to1"])
                            temp[item["locus2_id"]]["jitter_up"].insert(0, item["jitter_1to2"])
                            temp[item["locus2_id"]]["latency_down"].insert(0, item["latency_median_2to1"])
                            temp[item["locus2_id"]]["latency_up"].insert(0, item["latency_median_1to2"])
                    else:#se não achar o nome do locus 1
                        if not (item["locus1_id"] in temp):#se não achar o id do locus 1
                            temp[item["locus1_id"]] = {
                                "name": item["locus1_id"],
                                "jitter_down": [item["jitter_1to2"]],
                                "jitter_up": [item["jitter_2to1"]],
                                "latency_down": [item["latency_median_1to2"]],
                                "latency_up": [item["latency_median_2to1"]]
                            }
                        else:#se o id do locus 1 ja estiver na lista, apenas insere novos valores a ela
                            temp[item["locus1_id"]]["jitter_down"].insert(0, item["jitter_1to2"])
                            temp[item["locus1_id"]]["jitter_up"].insert(0, item["jitter_2to1"])
                            temp[item["locus1_id"]]["latency_down"].insert(0, item["latency_median_1to2"])
                            temp[item["locus1_id"]]["latency_up"].insert(0, item["latency_median_2to1"])

               
                if (len(id_array)==0):
                    response["id_last_item"] = id_last_item

                


                else:
                    response["id_last_item"] = max(id_array)
                
                
                response["links"] = list() #uma lista com os links é inicializada
                for index in temp:
                    response["links"].append(temp[index])#temp (a lista formada acima) é posta na lista dos links

                macs = list(KPIWireless.objects.order_by().values("mac").distinct())#


                wireless = list()
                for mac in macs:
                    last_device_data = KPIWireless.objects.filter(Q(locus=locus) & Q(mac=mac["mac"]), timestamp__gt=wireless_time_threshold).values().last()
                    wireless.append(last_device_data)


                if wireless:
                    response["wireless"] = wireless

            except Exception as e:
                return JsonResponse({"error2": str(e)})

            if "last" in request.GET and request.GET["last"] != "":
                last_records = int(request.GET["last"])
                try:
                    response["measurements"] = response["measurements"][
                                               :int(last_records)]
                except Exception as e:
                    return JsonResponse({"error": str(e)})

            response["success"] = "dashboardlinks"

        else:
            response["error"] = "Method not allowed"

        return JsonResponse(response)


    @staticmethod
    @csrf_exempt
    def kpilink(request):
        """KPI measurements.
        """
        response = dict()
        if request.method == "GET":

            try:
                required_fields = ["locus"]
                RestFunctions.check_required_fields(required_fields,
                                                    request.GET)
            except Exception as e:
                return JsonResponse({"error": str(e)})

            try:
                locus = Pool.objects.get(name=request.GET["locus"])
            except ObjectDoesNotExist:
                return JsonResponse({"error": "Pool not registered"})

            try:
                response["measurements"] = list(
                        KPILink.objects.filter(locus1=locus)
                        .order_by("-timestamp")
                        .values())
            except Exception as e:
                return JsonResponse({"error": str(e)})

            if "last" in request.GET and request.GET["last"] != "":
                last_records = int(request.GET["last"])
                try:
                    response["measurements"] = response["measurements"][
                                               :int(last_records)]
                except Exception as e:
                    return JsonResponse({"error": str(e)})

            response["success"] = "kpilink"

        elif request.method == "POST":
            try:
                required_fields = ["locus1", "locus2", "jitter_1to2",
                                   "latency_max_1to2", "latency_median_1to2",
                                   "latency_min_1to2", "jitter_2to1",
                                   "latency_max_2to1", "latency_median_2to1",
                                   "latency_min_2to1", "throughput"]

                RestFunctions.check_required_fields(required_fields,
                                                    request.POST)
            except Exception as e:
                return JsonResponse({"error": str(e)})

            try:
                locus1 = Pool.objects.get(name=request.POST["locus1"])
                locus2 = Pool.objects.get(name=request.POST["locus2"])
            except Exception as e:
                return JsonResponse({"error": str(e)})

            try:
                KPILink(locus1=locus1,
                        locus2=locus2,
                        jitter_1to2=request.POST["jitter_1to2"],
                        latency_max_1to2=request.POST["latency_max_1to2"],
                        latency_median_1to2=request.POST["latency_median_1to2"],
                        latency_min_1to2=request.POST["latency_min_1to2"],
                        jitter_2to1=request.POST["jitter_2to1"],
                        latency_max_2to1=request.POST["latency_max_2to1"],
                        latency_median_2to1=request.POST["latency_median_2to1"],
                        latency_min_2to1=request.POST["latency_min_2to1"],
                        throughput=request.POST["throughput"]).save()
            except Exception as e:
                response["error"] = str(e)

            response["success"] = "post_kpilink"

        else:
            response["error"] = "Method not allowed"

        return JsonResponse(response)

    # KPI COMMAND
    @staticmethod
    @csrf_exempt
    def kpicommand(request):
        """Command measurements
        """
        response = dict()
        if request.method == "GET":
            try:
                required_fields = ["locus"]
                RestFunctions.check_required_fields(required_fields,
                                                    request.GET)
            except Exception as e:
                return JsonResponse({"error": str(e)})

            try:
                locus = Pool.objects.get(name=request.GET["locus"])
            except Exception as e:
                return JsonResponse({"Error": str(e)})

            try:
                response["measurements"] = list(
                        KPICommand.objects.filter(locus=locus)
                        .order_by("-timestamp")
                        .values())
            except Exception as e:
                return JsonResponse({"error": str(e)})

            if "last" in request.GET and request.GET["last"] != "":
                last_records = request.GET["last"]
                try:
                    response["measurements"] = response["measurements"][
                                               :int(last_records)]
                except Exception as e:
                    return JsonResponse({"error": str(e)})

            response["success"] = "kpicommand"

        elif request.method == "POST":
            try:
                required_fields = ["locus", "cmd", "cmd_type",
                                   "proc_time", "response_time"]
                RestFunctions.check_required_fields(required_fields,
                                                    request.POST)
            except Exception as e:
                return JsonResponse({"error": str(e)})

            try:
                locus = Pool.objects.get(name=request.POST["locus"])
            except Exception as e:
                return JsonResponse({"error": str(e)})

            try:
                KPICommand(locus=locus,
                           proc_time=request.POST["proc_time"],
                           response_time=request.POST["response_time"],
                           cmd=request.POST["cmd"],
                           cmd_type=request.POST["cmd_type"]).save()
            except Exception as e:
                response["error"] = str(e)

            response["success"] = "kpicommand"

        else:
            response["error"] = "Method not allowed"

        return JsonResponse(response)

    # KPI RESOURCE
    @staticmethod
    @csrf_exempt
    def kpiresource(request):
        """Request command measurements (Response time) from a Tier
        """
        response = dict()
        if request.method == "GET":
            try:
                required_fields = ["locus"]
                RestFunctions.check_required_fields(required_fields,
                                                    request.GET)
            except Exception as e:
                return JsonResponse({"error": str(e)})

            try:
                locus = Pool.objects.get(name=request.GET["locus"])
            except Exception as e:
                return JsonResponse({"Error": str(e)})

            try:
                response["measurements"] = list(
                        KPIResources.objects.filter(locus=locus)
                        .order_by("-timestamp")
                        .values())
            except Exception as e:
                return JsonResponse({"error": str(e)})

            if "last" in request.GET and request.GET["last"] != "":
                last_records = request.GET["last"]
                try:
                    response["measurements"] = response["measurements"][
                                               :int(last_records)]
                except Exception as e:
                    return JsonResponse({"error": str(e)})

            response["success"] = "kpiresource"

        elif request.method == "POST":
            try:
                required_fields = ["locus", "CPU", "memory"]
                RestFunctions.check_required_fields(required_fields,
                                                    request.POST)
            except Exception as e:
                return JsonResponse({"error": str(e)})

            try:
                locus = Pool.objects.get(name=request.POST["locus"])
            except Exception as e:
                return JsonResponse({"error": str(e)})

            try:
                KPIResources(locus=locus,
                             CPU=request.POST["CPU"],
                             memory=request.POST["memory"]).save()
            except Exception as e:
                response["error"] = str(e)

            response["success"] = "kpiresource"

        else:
            response["error"] = "Method not allowed"

        return JsonResponse(response)

    # KPI WIRELESS
    @staticmethod
    @csrf_exempt
    def kpiwireless(request):
        """Wireless KPI measurements
        """
        response = dict()
        if request.method == "GET":
            try:
                required_fields = ["locus"]
                RestFunctions.check_required_fields(required_fields,
                                                    request.GET)
            except Exception as e:
                return JsonResponse({"error": str(e)})

            try:
                locus = Pool.objects.get(name=request.GET["locus"])
            except Exception as e:
                return JsonResponse({"error": str(e)})

            try:
                response["measurements"] = list(
                        KPIWireless.objects.filter(locus=locus)
                        .order_by("-timestamp")
                        .values())
            except Exception as e:
                return JsonResponse({"error": str(e)})

            if "last" in request.GET and request.GET["last"] != "":
                last_records = request.GET["last"]
                try:
                    response["measurements"] = response["measurements"][
                                               :int(last_records)]
                except Exception as e:
                    return JsonResponse({"error": str(e)})

            response["success"] = "kpiwireless"

        elif request.method == "POST":
            register_array = json.loads(request.body.decode("utf-8"))
            
            try:
                required_fields = ["locus", "mac", "mfb", "tdls", "wmm",
                                   "authenticated", "authorized",
                                   "expected_throughput", "inactive_time",
                                   "preamble", "rx_bitrate", "rx_bytes",
                                   "rx_packets", "signal", "signal_avg",
                                   "tx_bitrate", "tx_bytes", "tx_failed",
                                   "tx_retries"]

                for register in register_array:
                    RestFunctions.check_required_fields(required_fields,
                                                        register)
                                                        
            except Exception as e:
                return JsonResponse({"error": str(e)})

            try:
                locus = Pool.objects.get(name=register_array[0]["locus"])
            except Exception as e:
                return JsonResponse({"error": str(e)})

            try:
                for register in register_array:
                    KPIWireless(locus=locus,
                                mac=register["mac"],
                                mfb=register["mfb"],
                                tdls=register["tdls"],
                                wmm=register["wmm"],
                                authenticated=register["authenticated"],
                                authorized=register["authorized"],
                                expected_throughput=register[
                                    "expected_throughput"],
                                inactive_time=register["inactive_time"],
                                preamble=register["preamble"],
                                rx_bitrate=register["rx_bitrate"],
                                rx_bytes=register["rx_bytes"],
                                rx_packets=register["rx_packets"],
                                signal=register["signal"],
                                signal_avg=register["signal_avg"],
                                tx_bitrate=register["tx_bitrate"],
                                tx_bytes=register["tx_bytes"],
                                tx_failed=register["tx_failed"],
                                tx_retries=register["tx_retries"]).save()
                                
            except Exception as e:
                response["error"] = str(e)

            response["success"] = "post_kpiwireless"

        else:
            response["error"] = "Method not allowed"

        return JsonResponse(response)

    @staticmethod
    @csrf_exempt
    def update_configuration(request):
        response = dict()
        if request.method == "POST":
            try:
                exp = Configuration.objects.get(name="default")
            except Exception as e:
                return JsonResponse({"error": str(e)})

            update_fields = []
            if "delegation_mode" in request.POST:
                new_delegation_mode = request.POST["delegation_mode"]
                if exp.delegation_mode != new_delegation_mode:
                    exp.delegation_mode = new_delegation_mode
                    update_fields += ["delegation_mode"]

            if "auto_delegation_type" in request.POST:
                new_auto_delegation_type = request.POST["auto_delegation_type"]
                if exp.auto_delegation_type != new_auto_delegation_type:
                    exp.auto_delegation_type = new_auto_delegation_type
                    update_fields += ["auto_delegation_type"]

            try:
                exp.save(update_fields=update_fields)
            except Exception as e:
                response["error"] = str(e)

            response["success"] = "update_configuration"

        elif request.method == "GET":  # TO BE TESTED!
            config = list(Configuration.objects.filter(name="default").values())
            response["configuration"] = config

        else:
            response["error"] = "Method not allowed"

        return JsonResponse(response)
