param(
    [String] $VMName,
    [Int64] $Minimum,
    [Int64] $Startup,
    [Int64] $Maximum,
    [Int32] $Priority,
    [Int32] $Buffer
)

Set-VMMemory -VMName $VMName -DynamicMemoryEnabled $true -MinimumBytes $Minimum -StartupBytes $Startup -MaximumBytes $Maximum -Priority $Priority -Buffer $Buffer | Write-Output