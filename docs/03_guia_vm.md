# Guía VM — Desempaquetado aav.exe / aavshield.exe

**VM:** Windows XP SP3 o 7 x86, sin red, snapshot limpio

1. Copiar `extracted/app/aav.exe`
2. x64dbg → File → aav.exe → BP `LoadLibraryA`, `GetProcAddress`
3. Run → trace hasta `pushad` / `jmp OEP` (típico Delphi packer)
4. Scylla → Dump + Fix Imports
5. IDR / DeDe sobre dump → buscar `TfrmMain` / `LoadBases` / `ScanFile`
6. BP `CreateFileA` con `aavbase.dat` → F7 hasta descifrado → dump memoria

No ejecutar `aavshield.exe` como servicio sin aislar.

## Herramientas
- DIE / PE-bear / ExeinfoPE
- x64dbg + Scylla
- IDR (Interactive Delphi Reconstructor)
