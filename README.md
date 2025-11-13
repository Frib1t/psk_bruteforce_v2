# 🧨 IKE PSK Bruteforce Helper

Script en Python 3 para **auditar pre-shared keys (PSK) de IKE/IPsec** utilizando la herramienta `ike-scan`.  
Está pensado para **entornos de laboratorio** y **auditorías autorizadas**, nunca para uso malintencionado.

> ⚠️ **Aviso legal**  
> El uso de esta herramienta contra sistemas sin autorización explícita puede ser ilegal.  
> El autor y los colaboradores no se hacen responsables del uso inadecuado que se haga de este código.  
> Úsalo **solo** en infraestructuras propias o donde tengas un permiso por escrito.

---

## 🚀 Características

- 🔁 **Bruteforce de PSK** usando `ike-scan` y una wordlist.
- 🧵 **Multihilo** mediante `ThreadPoolExecutor` (paraleliza los intentos).
- ⏱️ **Delay configurable** entre resultados para no saturar la salida.
- ⚙️ **Transform personalizable** (`--transform`) para ajustar los parámetros IKE.
- 📊 Muestra progreso en formato:  
  `[#actual / #total] PSK: <valor> → válida/inválida`
- 📜 Imprime la salida completa de `ike-scan` cuando encuentra una PSK válida.

---

## 📦 Requisitos

- **Python** 3.x
- Herramienta **[`ike-scan`](https://linux.die.net/man/1/ike-scan)** instalada y disponible en `$PATH`
- Un sistema tipo **Linux** (recomendado para usar `ike-scan`)
- Una **wordlist** de posibles PSK (una por línea)

Ejemplo de instalación de `ike-scan` en Debian/Ubuntu/Kali:

```bash
sudo apt update
sudo apt install ike-scan
```

---

# 🧩 Instalación

Clona el repositorio y entra en la carpeta:
```bash
git clone https://github.com/Frib1t/psk_bruteforce_v2.git
```
```bash
cd psk_bruteforce_v2
```

Haz el script ejecutable si quieres lanzarlo como binario:
```bash
chmod +x psk_bruteforce_v2.py
```

Opcional: crear un entorno virtual para aislar dependencias:
```bash
python3 -m venv venv
source venv/bin/activate
```
---

# 🧭 Menú de uso rápido

- Identifica la IP o FQDN de la puerta de enlace IKE/IPsec que estés autorizado a auditar.
- Prepara una wordlist de PSK (.txt) con una clave por línea.
- Lanza el script indicando:
  - el objetivo (-t / --target)
  - la wordlist (-w / --wordlist)

Ajusta opcionalmente:
  - número de hilos (--threads)
  - delay entre resultados (--delay)
  - transform de IKE (--transform)

Revisa la salida:
- PSK válidas marcadas como VÁLIDA
- resumen final con todas las PSK encontradas

--- 

# 🛠️ Uso
## Sintaxis básica:
```bash
python3 psk_bruteforce_v2.py -t <IP_O_DOMINIO> -w <RUTA_WORDLIST>
```

## Parámetros
| Opción             | Obligatorio | Descripción                                                      |
| ------------------ | ----------: | ---------------------------------------------------------------- |
| `-t`, `--target`   |           ✅ | IP o dominio del objetivo IKE/IPsec.                             |
| `-w`, `--wordlist` |           ✅ | Fichero con la lista de PSKs a probar (una por línea).           |
| `--transform`      |           ❌ | Transform de IKE a usar (por defecto: `5,2,1,2`).                |
| `--threads`        |           ❌ | Número de hilos en paralelo (por defecto: `5`).                  |
| `--delay`          |           ❌ | Pausa (en segundos) entre líneas de salida (por defecto: `0.5`). |


## Ejecuta ayuda con:
```bash
python3 psk_bruteforce_v2.py -h
```
---

# 📚 Ejemplos
1️⃣ Escaneo básico con wordlist
```bash
python3 psk_bruteforce_v2.py -t 192.0.2.10 -w wordlists/psk_top100.txt
```

2️⃣ Cambiar el transform de IKE
```bash
python3 psk_bruteforce_v2.py -t vpn.ejemplo.local -w wordlists/psk_corp.txt --transform 5,2,2,2
```

3️⃣ Más hilos + menos delay (⚠️ más agresivo)
```bash
python3 psk_bruteforce_v2.py -t 192.0.2.10 -w wordlists/psk_big.txt --threads 15 --delay 0.1
```

## ⚠️ Ten en cuenta que aumentar el número de hilos puede:
- Generar más ruido en logs
- Activar mecanismos de defensa
- Impactar en la estabilidad del servicio objetivo

## 🧾 Formato de salida
Durante la ejecución, verás líneas tipo:
```bash
[     1/1000] PSK: claveSuperSecreta   → inválida
[     2/1000] PSK: empresa2024!        → VÁLIDA
============================================================
<salida completa de ike-scan>
[+] ¡PSK ENCONTRADA: empresa2024! 
============================================================
```

Al final, resumen:
```bash
[+] ¡ÉXITO! PSKs válidas: 1
    → empresa2024!
```
O bien, si no hay coincidencias:
```bash
[!] Ninguna PSK encontrada en 1000 intentos.
```

---

# 🔐 Uso responsable
Esta herramienta está creada con fines de:
  🔎 Auditoría de seguridad en entornos profesionales con autorización.
  🎓 Formación en laboratorios y entornos controlados.
  🛡️ Verificación de la robustez de PSK en infraestructuras propias.

No la uses nunca contra sistemas de terceros sin un permiso explícito y por escrito.

---

# 🧭 Roadmap / Ideas de mejora
Algunas mejoras que se podrían implementar en futuras versiones:
  - --output para guardar PSK válidas en fichero.
  - --stop-on-first para detener el script al encontrar la primera clave válida.
  - --quiet / --verbose para ajustar el nivel de detalle.
  - Sistema de reanudación (resume) para wordlists muy grandes.
  - Colores en la salida para destacar estados (válida/errónea/timeout).
  - Estadísticas al final: tiempo total, intentos/segundo, etc.

---

# Pull Requests son bienvenidos 💚
# 👤 Autor
- Script y concepto: (Ramón Frizat akka Frib1t)
- Lenguaje: Python 3
- Dependencia principal: ike-scan
- Si usas este proyecto en tus labs o formaciones, una mención o estrellita ⭐ en el repo siempre se agradece 🙂
