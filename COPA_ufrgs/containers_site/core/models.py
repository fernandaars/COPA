from django.db import models

from django.urls import reverse


# Create your models here.
class Configuration(models.Model):
    name = models.CharField(max_length=50,
                            default="default",
                            editable=False,
                            primary_key=True,
                            help_text="Configuration name.")
    DELEGATION_CHOICES = (("a", "Automatic"),
                          ("m", "Manual"))
    delegation_mode = models.CharField(max_length=1,
                                       choices=DELEGATION_CHOICES,
                                       help_text="Delegation mode (a - "
                                                 "Automatic; m - Manual).",
                                       blank=False,
                                       default="m")
    auto_delegation_type = models.CharField(max_length=100,
                                            help_text="Automatic delegation "
                                                      "type.",
                                            blank=True,
                                            null=True)

    def get_absolute_url(self):
        return reverse("configuration_detail",
                       args=[str(self.name)])

    def __str__(self):
        return self.name


class Pool(models.Model):
    name = models.CharField(max_length=50,
                            help_text="Pool name.",
                            primary_key=True)
    tier_class = models.ForeignKey(to='TierClass',
                                   on_delete=models.SET_NULL,
                                   null=True,
                                   blank=True)
    configuration = models.ForeignKey(to='Configuration',
                                      on_delete=models.CASCADE,
                                      default="default",
                                      editable=False)
    local_ip = models.GenericIPAddressField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("locus_detail",
                       args=[str(self.name)])

    class Meta:
        ordering = ["name"]


class TierClass(models.Model):
    configuration = models.ForeignKey(to='Configuration',
                                      on_delete=models.CASCADE,
                                      default="default",
                                      editable=False)
    name = models.CharField(max_length=50,
                            help_text="Tier name.")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]

    def get_absolute_url(self):
        return reverse("tierclass_detail",
                       args=[str(self.id)])


class Container(models.Model):
    pool = models.ForeignKey(to='Pool',
                             on_delete=models.SET_NULL,
                             blank=True,
                             null=True)
    name = models.CharField(max_length=100,
                            null=True,
                            blank=True)
    description = models.CharField(max_length=100,
                                   null=True,
                                   blank=True)
    pid = models.BigIntegerField(null=True,
                                 blank=True)
    status = models.CharField(max_length=20,
                              null=True,
                              blank=True)
    usage_memory = models.BigIntegerField(null=True,
                                          blank=True)
    usage_memory_peak = models.BigIntegerField(null=True,
                                               blank=True)
    usage_swap = models.BigIntegerField(null=True,
                                        blank=True)
    usage_swap_peak = models.BigIntegerField(null=True,
                                             blank=True)
    cpu_usage = models.BigIntegerField(null=True,
                                       blank=True)
    processes = models.IntegerField(null=True,
                                    blank=True)
    full_network_info = models.TextField(null=True,
                                         blank=True)
    created = models.DateTimeField(auto_now_add=True,
                                   editable=False)
    last_update = models.DateTimeField(auto_now_add=True,
                                       editable=False)

    def __str__(self):
        return self.name


class Image(models.Model):
    alias = models.CharField(max_length=50,
                             help_text="Tier name.",
                             unique=True)
    fingerprint = models.CharField(max_length=64,
                                   help_text="Tier name.",
                                   unique=True)

    def __str__(self):
        return self.alias

    class Meta:
        ordering = ["alias"]
