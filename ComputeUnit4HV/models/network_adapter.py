import os

from django.db import models
from ComputeUnit4HV.executor import executor as Execute


class AbstractNetworkAdapter(models.Model):
    vm_name = models.CharField(max_length=100)
    vm_id = models.UUIDField()
    host_name = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    switch_name = models.CharField(max_length=100)
    switch_id = models.UUIDField()
    mac_address = models.CharField(max_length=100)
    bandwidth_maximum = models.CharField(max_length=100)
    bandwidth_minimum = models.CharField(max_length=100)

    class Meta:
        abstract = True

    def get_network_adapter(self):
        ps_script = '%s\\scripts\\network_adapter\\get_network_adapter.ps1' % os.path.dirname(os.path.abspath(__file__))
        param = '''
                -VMName %s
                ''' % self.vm_name
        command = ps_script + ' ' + param
        result = Execute.execute_command(command, convert_to_json=True)
        return result
