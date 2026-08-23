# Proceso VM — Documentado en VMWare Workstation Pro 26H1

> El investigador determinó que VMWare resulta más estable que VirtualBox (problemas de rendimiento y bloqueos) e Hyper-V (inversión del cursor).

## Secuencia (vinculada a Screenshots/*.png)

1. **Instalación de VMWare Workstation Pro 26H1** — `Screenshots/1.png`
2. **Instalación de XP Professional SP3 sin internet** — `Screenshots/2.png`
3. **Compartición de carpeta mediante VMWare Tools** — `Screenshots/3.png`
4. **Copia del contenido a `C:\Abacre\`** — `Screenshots/4.png`
5. **Apertura de `aav.exe`** — `Screenshots/5.png`
6. **Obtención del PID en Administrador de tareas** (columna PID activada) — `Screenshots/6.png`
7. **Ejecución de `ntsd -pv -p <PID>` en CMD** — `Screenshots/7.png`
8. **Creación del dump: `.dump aav.dmp` (mini, 11 KB) o `.dump /f aav_fulldump.dmp` (full, 29 MB)** — se escribe sin ruta para evitar error 123, quedando en `C:\Documents and Settings\Daniel\` — `Screenshots/8.png`, `9.png`
9. **Salida con `q` → Enter** — `Screenshots/9.png`
10. **Generación completada** — dumps en `analysis/aavbase/` — `Screenshots/10.png`

## Observaciones
- Windows 7 no resultó compatible con Abacre; se requiere XP SP3.
- La ruta con directorio provocaba error 123 (`a:Abacre`); se soluciona omitiendo el directorio.
- Los scripts posteriores se encuentran en `scripts/` y la ejecución completa en `scripts/run_all.ps1`.
