import os
import uuid

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from ComputeUnit4HV.executor import executor as Execute


class AbstractSwitch(models.Model):
    switch_name = models.CharField(max_length=100)
    # The JSON type output callback switch type an int, not a string
    # 0 is Private, 1 is Internal, 2 is External
    switch_type = models.IntegerField()
    switch_id = models.UUIDField(default=uuid.uuid4)
    host_name = models.CharField(default='unknown', max_length=100)

    class Meta:
        abstract = True

    def new_switch(self):
        pass

    def get_switch(self):
        ps_script = '%s' % Execute.get_script_path('network\\switch\\get_switch.ps1')
        param = '-Name %s' % self.switch_name
        command = ps_script + ' ' + param
        result = Execute.execute_command(command, convert_to_json=True)
        return result

    def remove_switch(self):
        ps_script = '%s' % Execute.get_script_path('network\\switch\\remove_switch.ps1')
        param = '-SwitchName %s' % self.switch_name
        command = ps_script + ' ' + param
        result = Execute.execute_command(command, convert_to_json=False)
        if 'CategoryInfo' not in result:
            return True
        else:
            raise Exception(result)


class PrivateSwitch(AbstractSwitch):

    def new_switch(self):
        ps_script = '%s' % Execute.get_script_path('network\\switch\\new_switch_private.ps1')
        param = '-SwitchName %s' % self.switch_name
        command = ps_script + ' ' + param
        result = Execute.execute_command(command, convert_to_json=True)
        if 'CategoryInfo' not in result:
            import json
            try:
                json_data = json.loads(result)
                self.switch_id = json_data.get('Id', uuid.uuid4())
                self.host_name = json_data['ComputerName']
                self.switch_type = json_data['SwitchType']
            except json.JSONDecodeError:
                raise json.JSONDecodeError
            self.save(force_update=True)
            return True
        else:
            raise Exception(result)


class InternalSwitch(AbstractSwitch):

    def new_switch(self):
        ps_script = '%s' % Execute.get_script_path('network\\switch\\new_switch_internal.ps1')
        param = '-SwitchName %s' % self.switch_name
        command = ps_script + ' ' + param
        result = Execute.execute_command(command, convert_to_json=True)
        if 'CategoryInfo' not in result:
            import json
            try:
                json_data = json.loads(result)
                self.switch_id = json_data.get('Id', uuid.uuid4())
                self.host_name = json_data['ComputerName']
                self.switch_type = json_data['SwitchType']
            except json.JSONDecodeError:
                raise json.JSONDecodeError
            self.save(force_update=True)
            return True
        else:
            raise Exception(result)


class ExternalSwitch(AbstractSwitch):
    adapter_name = models.CharField(max_length=100)
    allow_host_use_adapter = models.BooleanField()

    def new_switch(self):
        ps_script = '%s' % Execute.get_script_path('network\\switch\\new_switch_external.ps1')
        if self.allow_host_use_adapter:
            self.allow_host_use_adapter = '1'
        else:
            self.allow_host_use_adapter = '0'
        param = '-SwitchName %s -AdapterName %s -AllowHostUseAdapter %s' % (self.switch_name, self.adapter_name, self.allow_host_use_adapter)
        command = ps_script + ' ' + param
        result = Execute.execute_command(command, convert_to_json=True)
        if 'CategoryInfo' not in result:
            import json
            callback = self.get_switch()
            try:
                json_data = json.loads(callback)
                self.switch_id = json_data.get('Id', uuid.uuid4())
                self.host_name = json_data['ComputerName']
                self.switch_type = json_data['SwitchType']
            except json.JSONDecodeError:
                raise json.JSONDecodeError
            self.save(force_update=True)
            return True
        else:
            raise Exception(result)

    def set_switch_external(self):
        ps_script = '%s\\scripts\\switch\\set_switch_external.ps1' % os.path.dirname(os.path.abspath(__file__))
        param = '-SwitchName %s -AdapterName %s -AllowHostUseAdapter %s' % (self.switch_name, self.adapter_name, self.allow_host_use_adapter)
        command = ps_script + ' ' + param
        result = Execute.execute_command(command, convert_to_json=False)
        if 'CategoryInfo' not in result:
            # TODO: Update the switch object

            return True
        else:
            raise Exception(result)


# TODO: Use queue tools to create a queue for the switch creation
@receiver(post_save, sender=PrivateSwitch)
def create_private_switch(sender, instance, created, **kwargs):
    if created:
        result = instance.new_switch()


@receiver(post_save, sender=InternalSwitch)
def create_internal_switch(sender, instance, created, **kwargs):
    if created:
        result = instance.new_switch()


@receiver(post_save, sender=ExternalSwitch)
def create_external_switch(sender, instance, created, **kwargs):
    if created:
        result = instance.new_switch()
