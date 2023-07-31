param(
    [String] $SwitchName,
    [String] $AdapterName,
    [Boolean] $AllowHostUseAdapter,
    [Parameter(Mandatory=$false)]
    [Int32] $VlanId
)
if ($AllowHostUseAdapter) {
    # if vlan id is specified, create a vlan switch
    # I don't find a way to configuration vlan id for a switch, so this is a workaround
    # TODO: find a way to configuration vlan id for a switch
    Set-VMSwitch -Name $SwitchName -NetAdapterName $AdapterName -AllowManagementOS $AllowHostUseAdapter | Write-Output
} else {
    # host can not use this adapter, so the vlan is not working
    Set-VMSwitch -Name $SwitchName -NetAdapterName $AdapterName -AllowManagementOS $AllowHostUseAdapter | Write-Output
}