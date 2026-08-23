# Guía VM — Resumen

Se requiere una VM Windows XP SP3 x86 sin red, con instantánea `limpio`.

1. Se instala el toolchain en `C:\tools\`: x64dbg (o OllyDbg 1.10 para XP), PE-bear/DIE, IDR, HxD. `vc_redist.x86.exe` se instala si aparece `api-ms-win-crt-runtime`.
2. Se verifica el packing: `die.exe aav.exe` debe indicar `Delphi + packed`.
3. El desempaquetado se realiza mediante `ntsd -pv -p <PID>` → `.dump /f aav_fulldump.dmp` (29 MB), evitando breakpoints que activan `Protection Error 251`.
4. El dump se copia a `analysis/aavbase/` y se analiza con `scripts/`.

El procedimiento detallado se encuentra en `04_guia_vm_completa.md` y la evidencia en `Screenshots/`.
