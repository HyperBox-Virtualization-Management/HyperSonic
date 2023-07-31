param(
    [String] $SwitchName,
    [String] $AdapterName,
    [Boolean] $AllowHostUseAdapter
)

New-VMSwitch -Name $SwitchName -NetAdapterName $AdapterName | Set-VMSwitch -AllowManagementOS $AllowHostUseAdapter | Write-Output