param(
    [String] $VMName,
    [Int64] $Count,
    [Boolean] $CompatibilityForOlderOS,
    [Int64] $Maximum,
    [Int64] $Reserve,
    [Int32] $RelativeWeight
)

Set-VMProcessor -VMName $VMName -Count $Count -CompatibilityForOlderOperatingSystemsEnabled $CompatibilityForOlderOS -Maximum $Maximum -Reserve $Reserve -RelativeWeight $RelativeWeight | Write-Output