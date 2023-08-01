import os
import uuid

from django.db import models
from ComputeUnit4HV.executor.abstract_executor import Execute


class AbstractSwitch(models.Model):
    host_name = models.CharField(max_length=100)
    switch_name = models.CharField(max_length=100)
    switch_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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
    adapter_name = models.CharField(max_length=100)
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
