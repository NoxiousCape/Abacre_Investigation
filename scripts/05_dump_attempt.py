import pathlib, pefile
# Intento estatico de extraer .data descifrable (sin ejecucion) - limitado por packing
for name in ["aav.exe","aavshield.exe"]:
    p = pathlib.Path(f"C:/Users/Usuario/Documents/Visual Studio 2022/Projects/Abacre_Inv/_extracted/app/{name}")
    pe=pefile.PE(str(p))
    # buscar seccion .data que podria contener key
    for s in pe.sections:
        if b".data" in s.Name:
            d=s.get_data()
            print(f"{name} .data {len(d)} bytes preview {d[:32].hex(' ')}")
            # guardar para analisis offline
            pathlib.Path(f"C:/Users/Usuario/Documents/Visual Studio 2022/Projects/Abacre_Inv/scripts_forense/{name}.data.bin").write_bytes(d)
            print(f" -> guardado {name}.data.bin")
