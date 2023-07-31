param(
    [String] $SwitchName
)

Remove-VMSwitch -Name $SwitchName -Force | Write-Output