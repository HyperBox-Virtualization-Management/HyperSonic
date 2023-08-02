import os

from django.db import models
from ComputeUnit4HV.executor import executor as Execute


class Processor(models.Model):
    vm_name = models.CharField(max_length=100)
    vm_id = models.UUIDField()
    host_name = models.CharField(max_length=100)
    count = models.IntegerField()
    compatibility_for_older_os = models.BooleanField()
    maximum = models.IntegerField()
    reserve = models.IntegerField()
    relative_weight = models.IntegerField()

    def set_processor(self):
        ps_script = '%s\\scripts\\processor\\set_processor.ps1' % os.path.dirname(os.path.abspath(__file__))
        param = '''
        -VMName %s 
        -Count %s 
        -CompatibilityForOlderOS %s 
        -Maximum %s
        -Reserve %s 
        -RelativeWeight %s
        ''' % (
            self.vm_name, self.count, self.compatibility_for_older_os, self.maximum, self.reserve, self.relative_weight)
        command = ps_script + ' ' + param
        result = Execute.execute_command(command, convert_to_json=False)
        if result == "":
            return True
        else:
            return result

    def get_processor(self):
        ps_script = '%s\\scripts\\processor\\get_processor.ps1' % os.path.dirname(os.path.abspath(__file__))
        param = '''
                -VMName %s
                ''' % self.vm_name
        command = ps_script + ' ' + param
        result = Execute.execute_command(command, convert_to_json=True)
        return result

