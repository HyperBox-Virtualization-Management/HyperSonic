param(
    [String] $SwitchName
)

New-VMSwitch -Name $SwitchName -SwitchType Internal | Write-Output