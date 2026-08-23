# Repro completo
# Extraccion
tools\innoextract.exe --info original\setup.exe
tools\innoextract.exe --list --list-sizes original\setup.exe
tools\innoextract.exe --extract --output-dir extracted original\setup.exe
# Analisis
python scripts\01_analyze_aavbase.py
python scripts\02_analyze_aavshield.py
python scripts\03_statistical_crypto.py > analysis\aavbase\statistical.txt
python scripts\04_find_decrypt.py
python scripts\05_dump_attempt.py
