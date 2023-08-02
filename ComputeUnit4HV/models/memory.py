import os

from django.db import models
from ComputeUnit4HV.executor import executor as Execute


class AbstractMemory(models.Model):
    vm_name = models.CharField(max_length=100)
    vm_id = models.UUIDField()
    host_name = models.CharField(max_length=100)
    dynamic_memory = models.BooleanField()
    startup_bytes = models.CharField(max_length=100)
    priority = models.IntegerField()

    class Meta:
        abstract = True

    def get_memory(self):
        ps_script = '%s\\scripts\\memory\\get_memory.ps1' % os.path.dirname(os.path.abspath(__file__))
        param = '''
                -VMName %s
                ''' % self.vm_name
        command = ps_script + ' ' + param
        result = Execute.execute_command(command, convert_to_json=True)
        return result


class DynamicMemory(AbstractMemory):
    minimum_bytes = models.CharField(max_length=100)
    maximum_bytes = models.CharField(max_length=100)
    buffer = models.IntegerField()

    def set_memory(self):
        self.dynamic_memory = True
        ps_script = '%s\\scripts\\memory\\set_memory_dynamic.ps1' % os.path.dirname(os.path.abspath(__file__))
        param = '''
                -VMName %s
                -Minimum %s
                -Startup %s
                -Maximum %s
                -Priority %s
                -Buffer %s
                ''' % (
            self.vm_name, self.minimum_bytes, self.startup_bytes, self.maximum_bytes, self.priority, self.buffer)
        command = ps_script + ' ' + param
        result = Execute.execute_command(command, convert_to_json=False)
        if result == "":
            return True
        else:
            return result


class StaticMemory(AbstractMemory):

    def set_memory(self):
        self.dynamic_memory = False
        # When memory is static, the Minimum, Maximum and Buffer not used.
        ps_script = '%s\\scripts\\memory\\set_memory_static.ps1' % os.path.dirname(os.path.abspath(__file__))
        param = '''
                -VMName %s
                -Startup %s
                -Priority %s
                ''' % (self.vm_name, self.startup_bytes, self.priority)
        command = ps_script + ' ' + param
        result = Execute.execute_command(command, convert_to_json=False)
        if result == "":
            return True
        else:
            return result
