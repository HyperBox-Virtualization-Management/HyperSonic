param(
    [String] $Name
)

Get-VMSwitch -Name $Name | Write-Output
