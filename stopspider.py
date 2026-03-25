# stop_spider.py
try:
    import psutil  # type: ignore[reportMissingImports]
except ImportError as e:
    raise RuntimeError(
        "psutil non risulta installato nell'ambiente Python corrente. "
        "Esegui `python spider_runner.py setup` e riprova."
    ) from e
import os

TARGET_NAMES = {"spider", "spider.exe", "spider.py"}

def main():
    current_pid = os.getpid()
    killed = 0

    for proc in psutil.process_iter(["pid", "name", "cmdline"]):
        try:
            if proc.info["pid"] == current_pid:
                continue

            name = (proc.info["name"] or "").lower()
            cmdline = " ".join(proc.info.get("cmdline") or []).lower()

            if any(t in name for t in TARGET_NAMES) or any(t in cmdline for t in TARGET_NAMES):
                proc.kill()
                killed += 1
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    print(f"Processi ragno terminati: {killed}")


if __name__ == "__main__":
    main()