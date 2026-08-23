# Abacre Antivirus 1.3 — Ingeniería Inversa Académica

> **Fines exclusivamente académicos y de investigación.** Análisis estático de un antivirus histórico (2006) que obtuvo 0% de detección en pruebas independientes.

## Contexto
Abacre Antivirus v1.3 (Inno Setup 5.1.2) — estudio de por qué falló en tests de 113.334 y 58 productos. Código Delphi empaquetado + base de firmas cifrada.

## Estructura
```
original/          # Instalador original y hashes SHA256
extracted/app/     # Payload extraído con innoextract 1.9
  aav.exe          # GUI principal (Delphi packed)
  aavshield.exe    # Resident shield (packed)
  aavbase.dat      # Base de firmas cifrada (15 KB)
scripts/           # Scripts forense reproducibles
docs/              # Informes técnicos
analysis/          # hashes, entropía, PE
tools/             # innoextract
```

## Hallazgos rápidos
- **Installer:** Inno Setup 5.1.2, `7EB44CC2...` (1362759 B)
- **Packing:** 11 secciones vacías, entropía 7.99, imports `LoadLibraryA/GetProcAddress` → desempaquetado dinámico requerido
- **aavbase.dat:** 15141 B, entropía 7.9876, stream cipher (no zlib), 256/256 bytes uniformes
- **Siguiente paso:** VM + x64dbg → OEP → Scylla → IDR → `CreateFileA("aavbase.dat")` → dump descifrado

## Uso
```powershell
# 1. Extraer
tools\innoextract.exe --extract --output-dir extracted original\setup.exe
# 2. Analizar
python scripts\01_analyze_aavbase.py
python scripts\03_statistical_crypto.py
```

## Disclaimer
No ejecutar binarios en host. Solo VM aislada sin red. Respetar licencia original.

## Referencias
- analysis/hashes.sha256
- docs/ (informes en generación)
