param(
    [String] $VMName
)

Get-VMProcessor -VMName $VMName | Write-Output