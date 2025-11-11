#!/usr/bin/env python3
import plotext as plt
import random

# 🎯 Data generator (no datetime, no external deps)
def get_data(period):
    random.seed(42)  # reproducible
    if period == "7d":
        days = 7
        base, drift, noise, thr = 110, 0.5, 3, 105
    elif period == "30d":
        days = 30
        base, drift, noise, thr = 105, 0.2, 5, 100
    elif period == "365d":
        days = 365
        base, drift, noise, thr = 100, 0.03, 8, 95
    else:  # "all" = 2 years
        days = 730
        base, drift, noise, thr = 95, 0.01, 10, 90

    caps = []
    for i in range(days):
        val = base + drift * i + random.uniform(-noise, noise)
        caps.append(round(max(80, val), 1))
    return caps, thr, days

def plot_chart(caps, threshold, period):
    plt.clf()
    plt.title(f"CS2 Market Cap | {period}")
    plt.xlabel("Days")
    plt.ylabel("$M")
    
    # Optimized for speed & clarity
    plt.plotsize(70, 16)        # compact but readable
    plt.theme("dark")
    plt.canvas_color("default")
    plt.axes_color("default")
    
    # Plot line
    plt.plot(caps, color="cyan", marker="fhd")  # "fhd" = full height dot (clean)
    
    # Threshold line
    plt.hline(threshold, color="red")
    
    # Smart x-ticks: show only key points
    n = len(caps)
    if n <= 30:
        ticks = list(range(0, n, max(1, n//7)))
    else:
        ticks = [0, n//4, n//2, 3*n//4, n-1]
    labels = [str(t+1) for t in ticks]
    plt.xticks(ticks, labels)
    
    # Y-ticks: 5 levels
    y_min, y_max = min(caps), max(caps)
    y_range = y_max - y_min
    y_step = max(5, round(y_range / 4))
    y_min_snap = ((y_min - 5) // y_step) * y_step
    y_max_snap = ((y_max + 5 + y_step - 1) // y_step) * y_step
    y_ticks = list(range(int(y_min_snap), int(y_max_snap)+1, y_step))
    plt.yticks(y_ticks)
    
    plt.ylim(y_min - 5, y_max + 5)
    plt.show()
    
    # Violation count
    violations = sum(1 for c in caps if c < threshold)
    status = "✅ PASS" if violations == 0 else f"⚠️ FAIL ({violations} days)"
    print(f"\n📊 {period:8} | Threshold: ${threshold}M | {status}")

def main():
    print("🎮 CS2 Market Cap Validator")
    print("[1] 7 Days   [2] 1 Month   [3] 1 Year   [4] All Time (2Y)   [Q] Quit")
    
    while True:
        choice = input("\n→ Select (1-4/q): ").strip().lower()
        if choice == 'q':
            print("👋 Bye!")
            break
        periods = {"1": "7d", "2": "30d", "3": "365d", "4": "all"}
        if choice in periods:
            period_name = {
                "7d": "7 Days",
                "30d": "1 Month",
                "365d": "1 Year",
                "all": "All Time"
            }[periods[choice]]
            print(f"\n⏳ Generating {period_name} chart...")
            caps, thr, _ = get_data(periods[choice])
            plot_chart(caps, thr, period_name)
        else:
            print("❌ Invalid. Try 1, 2, 3, 4, or q.")

if __name__ == "__main__":
    main()
