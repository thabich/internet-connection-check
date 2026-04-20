#!/usr/bin/env python3
import subprocess
import time
import random
from datetime import datetime
import speedtest

LOGFILE = "network_monitor.log"
PING_TARGET = "8.8.8.8"   # Google DNS

def log(message: str):
    with open(LOGFILE, "a") as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")

def ping_once():
    try:
        result = subprocess.run(
            ["ping", "-c", "1", PING_TARGET],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return result.returncode == 0
    except Exception as e:
        log(f"Ping error: {e}")
        return False

def cleanup(success_count):
    log(f"Last {success_count} pings were successful, terminating.")


def speedcheck():
    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        download = st.download() / 1_000_000  # Mbit/s
        upload = st.upload() / 1_000_000      # Mbit/s
        log(f"Speedcheck: {download:.2f} Mbit/s down / {upload:.2f} Mbit/s up")
    except Exception as e:
        log(f"Speedcheck error: {e}")

def main():
    success_count = 0
    next_speedcheck = time.time() + random.randint(1800, 2700)  # 30-45 min
    log(f"Starting connection check")
    last = time.time()
    try:
      while True:
          now = time.time()
          gap = now - last
          last = now
          if gap > 60:
             log(f"System resumed from suspend (gap {gap:.0f} sec), last {success_count} pings were successful before susped")
             success_count = 0
          else:
            if ping_once():
                success_count += 1
            else:
                log(f"Ping loss after {success_count} successful pings")
                success_count = 0

          if time.time() >= next_speedcheck:
              speedcheck()
              next_speedcheck = time.time() + random.randint(900, 1800)

          time.sleep(5)
    finally:
        cleanup(success_count)

if __name__ == "__main__":
    main()
