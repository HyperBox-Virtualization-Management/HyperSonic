import os

from django.db import models
from executor.abstract_executor import Execute


class Processor(models.Model):
    vm_name = models.CharField()
    vm_id = models.UUIDField()
    host_name = models.CharField()
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


# TODO: Abstract Memory class to AbstractMemory, and create two class DynamicMemory and StaticMemory
class Memory(models.Model):
    vm_name = models.CharField()
    vm_id = models.UUIDField()
    host_name = models.CharField()
    dynamic_memory = models.BooleanField()
    minimum_bytes = models.CharField()
    startup_bytes = models.CharField()
    maximum_bytes = models.CharField()
    priority = models.IntegerField()
    buffer = models.IntegerField()

    def set_memory(self):
        if self.dynamic_memory:
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
        else:
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

    def get_memory(self):
        ps_script = '%s\\scripts\\memory\\get_memory.ps1' % os.path.dirname(os.path.abspath(__file__))
        param = '''
                -VMName %s
                ''' % self.vm_name
        command = ps_script + ' ' + param
        result = Execute.execute_command(command, convert_to_json=True)
        return result


class AbstractSwitch(models.Model):
    host_name = models.CharField()
    switch_name = models.CharField()
    switch_id = models.CharField()
    # The JSON type output callback switch type an int, not a string
    # 0 is Private, 1 is Internal, 2 is External
    switch_type = models.IntegerField()

    class Meta:
        abstract = True

    def get_switch(self):
        ps_script = '%s\\scripts\\switch\\get_switch.ps1' % os.path.dirname(os.path.abspath(__file__))
        param = '''
                -Name %s
                ''' % self.switch_name
        command = ps_script + ' ' + param
        result = Execute.execute_command(command, convert_to_json=True)
        return result

    def remove_switch(self):
        ps_script = '%s\\scripts\\switch\\remove_switch.ps1' % os.path.dirname(os.path.abspath(__file__))
        param = '''
                -SwitchName %s
                ''' % self.switch_name
        command = ps_script + ' ' + param
        result = Execute.execute_command(command, convert_to_json=False)
        if result == "":
            return True
        else:
            return result


class PrivateSwitch(AbstractSwitch):

    def new_switch(self):
        self.switch_type = "Private"
        ps_script = '%s\\scripts\\switch\\new_switch_private.ps1' % os.path.dirname(os.path.abspath(__file__))
        param = '''
                -SwitchName %s
                ''' % self.switch_name
        command = ps_script + ' ' + param
        result = Execute.execute_command(command, convert_to_json=True)
        if self.switch_name in result:
            return True
        else:
            return result


class InternalSwitch(AbstractSwitch):

    def new_switch(self):
        self.switch_type = "Internal"
        ps_script = '%s\\scripts\\switch\\new_switch_internal.ps1' % os.path.dirname(os.path.abspath(__file__))
        param = '''
                -SwitchName %s
                ''' % self.switch_name
        command = ps_script + ' ' + param
        result = Execute.execute_command(command, convert_to_json=True)
        if self.switch_name in result:
            return True
        else:
            return result


class ExternalSwitch(AbstractSwitch):
    adapter_name = models.CharField()
    allow_host_use_adapter = models.BooleanField()

    def new_switch(self):
        self.switch_type = "External"
        ps_script = '%s\\scripts\\switch\\new_switch_external.ps1' % os.path.dirname(os.path.abspath(__file__))
        param = '''
                -SwitchName %s
                -AdapterName %s
                -AllowHostUseAdapter %s
                ''' % (self.switch_name, self.adapter_name, self.allow_host_use_adapter)
        command = ps_script + ' ' + param
        result = Execute.execute_command(command, convert_to_json=True)
        if self.switch_name in result:
            return True
        else:
            return result

    def set_switch(self):
        ps_script = '%s\\scripts\\switch\\set_switch_external.ps1' % os.path.dirname(os.path.abspath(__file__))
        param = '''
                -SwitchName %s
                -AdapterName %s
                -AllowHostUseAdapter %s
                ''' % (self.switch_name, self.adapter_name, self.allow_host_use_adapter)
        command = ps_script + ' ' + param
        result = Execute.execute_command(command, convert_to_json=False)
        if result == "":
            return True
        else:
            return result


class VirtualMachine(models.Model):
    name = models.CharField()
    id = models.UUIDField()
