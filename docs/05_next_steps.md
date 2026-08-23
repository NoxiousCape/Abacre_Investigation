# Próximos pasos

- El análisis estático y el dump de memoria se encuentran completados (ver `analysis/aavbase/aav_fulldump.dmp`).
- Se dispone de 70 firmas extraídas en `signatures.txt`.
- Pendiente queda el descifrado offline exacto de `aavbase.dat` (Blowfish, payload 15119 B no múltiplo de 8, posible padding/IV).
- Una vez obtenido el plaintext, se actualizará `analysis/aavbase/format.md` con la estructura `[Header][Registros]`.
