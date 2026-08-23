# Historial Bash / PowerShell utilizado
# 1 - Inspeccion inicial
Get-ChildItem -LiteralPath "Abacre_Inv" | Format-List
Get-FileHash -LiteralPath "Abacre_Inv/setup.exe"
# PE header
$bytes=[IO.File]::ReadAllBytes("setup.exe"); $peOffset=[BitConverter]::ToInt32($bytes,0x3C)
# 2 - Deteccion Inno Setup 5.1.2
Expand-Archive -Force -Path "innoextract.zip" -DestinationPath "innoextract_dir"
& "innoextract.exe" --info setup.exe
& "innoextract.exe" --list --list-sizes setup.exe
& "innoextract.exe" --extract --output-dir _extracted setup.exe
# 3 - Analisis PE
Analyze-PE "app/aav.exe"; Analyze-PE "app/aavshield.exe"
# 4 - Analisis aavbase.dat
python analyze_base.py
python analyze_shield.py
# 5 - Futuro
# python 03_statistical_crypto.py
# python 04_find_decrypt.py - requiere VM + x64dbg Scylla dump
