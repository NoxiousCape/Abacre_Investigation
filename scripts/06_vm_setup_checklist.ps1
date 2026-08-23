# VM Setup Checklist - Abacre RE
# Ejecutar DENTRO de VM Windows XP/7 x86

Write-Host "=== Abacre VM Checklist ===" -F Cyan
$tools = @("C:\tools\x64dbg\x32\x64dbg.exe","C:\tools\PE-bear\PE-bear.exe","C:\tools\IDR\idr.exe","C:\tools\Procmon.exe")
foreach($t in $tools){
  if(Test-Path $t){ Write-Host "[OK] $t" -F Green } else { Write-Host "[FALTA] $t" -F Red }
}
# Verificar snapshot
Write-Host "`n1. Verificar que red esta deshabilitada" -F Yellow
Get-NetAdapter | Format-Table Name,Status
Write-Host "`n2. Hash originals"
Get-FileHash C:\Abacre\original\setup.exe | FL
Write-Host "`n3. Listo para: bp LoadLibraryA + Scylla dump"
