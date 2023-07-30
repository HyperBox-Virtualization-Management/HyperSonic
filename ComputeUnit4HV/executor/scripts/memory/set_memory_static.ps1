param(
    [String] $VMName,
    [Int64] $Startup,
    [Int32] $Priority
)

Set-VMMemory -VMName $VMName -DynamicMemoryEnabled $false -StartupBytes $Startup -Priority $Priority | Write-Output