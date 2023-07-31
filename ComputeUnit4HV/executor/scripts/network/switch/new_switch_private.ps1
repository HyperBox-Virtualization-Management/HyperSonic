param(
    [String] $SwitchName
)

New-VMSwitch -Name $SwitchName -SwitchType Private | Write-Output