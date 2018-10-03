from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from core.models import Configuration, TierClass, Pool


# Create your views here.
def index(request):
    try:
        return redirect(Configuration.objects.get(name="default"))
    except ObjectDoesNotExist:
        return redirect("/monitor/configuration/create/")

def dashboard(request):
    return render(
        request,
        'dashboard.html'
    )

class ConfigurationDetailView(generic.DetailView):
    model = Configuration

    def get_queryset(self):
        return Configuration.objects.all()


class ConfigurationCreate(CreateView):
    model = Configuration
    fields = "__all__"


class ConfigurationUpdate(UpdateView):
    model = Configuration
    fields = "__all__"


class ConfigurationDelete(DeleteView):
    model = Configuration
    success_url = reverse_lazy("monitor_index")


class TierClassDetailView(generic.DetailView):
    model = TierClass


class TierClassCreate(CreateView):
    model = TierClass
    fields = "__all__"


class TierClassUpdate(UpdateView):
    model = TierClass
    fields = "__all__"


class TierClassDelete(DeleteView):
    model = TierClass
    success_url = reverse_lazy("monitor_index")


class LocusDetailView(generic.DetailView):
    model = Pool


class LocusCreate(CreateView):
    model = Pool
    fields = "__all__"

    def get_initial(self):
        if "pk" in self.kwargs:
            tier = TierClass.objects.get(pk=self.kwargs.get("pk"))
            return {"tier_class": tier}


class LocusUpdate(UpdateView):
    model = Pool
    fields = "__all__"


class LocusDelete(DeleteView):
    model = Pool
    success_url = reverse_lazy("monitor_index")
