from django.db import models


# CoLiSEU
class KPILink(models.Model):
    locus1 = models.ForeignKey(to='core.Pool',
                               on_delete=models.CASCADE)
    locus2 = models.ForeignKey(to='core.Pool',
                               related_name="locus2",
                               on_delete=models.CASCADE)
    jitter_1to2 = models.FloatField(help_text="Jitter from 1 to 2",
                                    blank=True,
                                    null=True)
    latency_max_1to2 = models.FloatField(help_text="Max Latency from 1 to 2",
                                         blank=True,
                                         null=True)
    latency_median_1to2 = models.FloatField(help_text="Median Latency "
                                                      "from 1 to 2",
                                            blank=True,
                                            null=True)
    latency_min_1to2 = models.FloatField(help_text="Min Latency from 1 to 2",
                                         blank=True,
                                         null=True)

    jitter_2to1 = models.FloatField(help_text="Jitter from 2 to 1",
                                    blank=True,
                                    null=True)
    latency_max_2to1 = models.FloatField(help_text="Max Latency from 2 to 1",
                                         blank=True,
                                         null=True)
    latency_median_2to1 = models.FloatField(
            help_text="Median Latency from 2 to 1",
            blank=True,
            null=True)
    latency_min_2to1 = models.FloatField(help_text="Min Latency from 2 to 1",
                                         blank=True,
                                         null=True)

    throughput = models.FloatField(help_text="Link Throughput",
                                   blank=True,
                                   null=True)
    timestamp = models.DateTimeField(auto_now_add=True,
                                     editable=False)

    def __str__(self):
        return str(self.pk)

    class Meta:
        ordering = ["timestamp"]


class KPIWireless(models.Model):
    locus = models.ForeignKey(to='core.Pool',
                              related_name="locus",
                              on_delete=models.CASCADE)
    mac = models.CharField(max_length=17,
                           blank=True,
                           help_text="MAC address", )
    mfb = models.BooleanField(default=False, help_text="")
    tdls = models.BooleanField(default=False, help_text="")
    wmm = models.BooleanField(default=False, help_text="")
    authenticated = models.BooleanField(default=False,
                                        help_text="Is authenticated?")
    authorized = models.BooleanField(default=False,
                                     help_text="Is authorized?")
    expected_throughput = models.CharField(max_length=10,
                                           blank=True,
                                           help_text="Expected link throughput")
    inactive_time = models.CharField(max_length=10,
                                     blank=True,
                                     help_text="Inactive time")
    preamble = models.CharField(max_length=10,
                                blank=True,
                                help_text="Preamble")
    rx_bitrate = models.CharField(max_length=20,
                                  blank=True,
                                  help_text="RX bitrate")
    rx_bytes = models.IntegerField(help_text="RX bytes")
    rx_packets = models.IntegerField(help_text="RX packets")
    signal = models.CharField(max_length=20,
                              blank=True,
                              help_text="Signal intensity")
    signal_avg = models.CharField(max_length=20,
                                  blank=True,
                                  help_text="Signal average")
    tx_bitrate = models.CharField(max_length=30,
                                  blank=True,
                                  help_text="TX bitrate", )
    tx_bytes = models.IntegerField(help_text="TX bytes")
    tx_failed = models.IntegerField(help_text="TX failed")
    tx_retries = models.IntegerField(help_text="TX retries")
    timestamp = models.DateTimeField(auto_now_add=True,
                                     editable=False)

    def __str__(self):
        return str(self.pk)

    class Meta:
        ordering = ["timestamp"]


# Experiment3.1
class KPICommand(models.Model):
    locus = models.ForeignKey(to='core.Pool',
                              on_delete=models.CASCADE)
    proc_time = models.FloatField(help_text="Processing time measurement",
                                  blank=True,
                                  null=True)
    response_time = models.FloatField(help_text="Response time measurement",
                                      blank=True,
                                      null=True)
    cmd = models.CharField(help_text="Command Issued",
                           max_length=200,
                           blank=True,
                           null=True)
    CMD_TYPE_CHOICES = (("v", "Voice"),
                        ("g", "Gesture"))
    cmd_type = models.CharField(max_length=1,
                                help_text="Command Type",
                                choices=CMD_TYPE_CHOICES,
                                blank=True,
                                null=True)
    timestamp = models.DateTimeField(auto_now_add=True,
                                     editable=False)

    def __str__(self):
        return str(self.pk)

    class Meta:
        ordering = ["timestamp"]


class KPIResources(models.Model):
    locus = models.ForeignKey(to='core.Pool',
                              on_delete=models.CASCADE)
    CPU = models.FloatField(help_text="CPU Load",
                            blank=True,
                            null=True)
    memory = models.FloatField(help_text="Memory usage",
                               blank=True,
                               null=True)
    timestamp = models.DateTimeField(auto_now_add=True,
                                     editable=False)

    def __str__(self):
        return str(self.pk)

    class Meta:
        ordering = ["timestamp"]
