import pathlib, collections, math, hashlib
p = pathlib.Path(r"C:\Users\Usuario\Documents\Visual Studio 2022\Projects\Abacre_Inv\_extracted\app\aavbase.dat")
b = p.read_bytes()[22:]
print(f"Payload: {len(b)} bytes SHA256 {hashlib.sha256(b).hexdigest()[:16]}...")
def entropy(d): 
    c=collections.Counter(d)
    return -sum(v/len(d)*math.log2(v/len(d)) for v in c.values())
print(f"Entropia global: {entropy(b):.4f}")
for w in [256,512,1024,2048]:
    ents=[entropy(b[i:i+w]) for i in range(0,len(b)-w,w)]
    print(f" Ventana {w}: min {min(ents):.3f} max {max(ents):.3f} avg {sum(ents)/len(ents):.3f}")
cnt=collections.Counter(b)
print(f"Bytes unicos: {len(cnt)}/256 chi2 uniform: {sum((v-len(b)/256)**2/(len(b)/256) for v in cnt.values()):.1f}")
pairs=collections.Counter(zip(b, b[1:]))
print(f"Pares unicos: {len(pairs)}/{len(b)-1} top3 {pairs.most_common(3)}")
# autocorrelacion lag 1..16
for lag in [1,2,4,8,16]:
    matches=sum(1 for i in range(len(b)-lag) if b[i]==b[i+lag])
    print(f" Autocorr lag {lag}: {matches} matches ({matches/(len(b)-lag)*100:.2f}%) esperado ~0.39%")
# test repetidos bloques
for bl in [16,32,64]:
    blocks=[b[i:i+bl] for i in range(0,len(b),bl)]
    uniq=len(set(blocks))
    print(f" Bloques {bl}B: {len(blocks)} total {uniq} unicos repetidos {len(blocks)-uniq}")
# comparativa RC4 vs AES indicios: RC4 sesgo primeros bytes, AES CTR no
print("Nota: 7.98 + 256/256 + sin repetidos = flujo cifrado (RC4/AES-CTR/XOR stream), no AES-CBC con padding")
