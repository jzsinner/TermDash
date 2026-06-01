#!/usr/bin/env python3
"""Terminal Dashboard for Your Daily Life."""

import json
import sys
from datetime import datetime
from pathlib import Path

import requests
from rich.console import Console
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.align import Align
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import box

# ========== CONFIGURATION ==========
CONFIG_FILE = Path.home() / ".dashboard_config.json"

DEFAULT_CONFIG = {
    "city": "London",  # Change to your city
    "units": "metric",  # metric or imperial
    "stocks": ["AAPL", "GOOGL", "TSLA"],
    "crypto": ["bitcoin", "ethereum"],
    "news_topics": ["technology", "programming"],
    "quotes": [
        "The only way to do great work is to love what you do.",
        "Stay hungry, stay foolish.",
        "It works on my machine ¯\\_(ツ)_/¯",
    ],
    "update_interval_seconds": 10,
}

# ========== UTILITIES ==========
console = Console()

def load_config():
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE) as f:
            user_config = json.load(f)
            return {**DEFAULT_CONFIG, **user_config}
    else:
        with open(CONFIG_FILE, "w") as f:
            json.dump(DEFAULT_CONFIG, f, indent=2)
        return DEFAULT_CONFIG

CONFIG = load_config()

def get_weather():
    """Fetch weather using wttr.in (no API key required)"""
    try:
        url = f"https://wttr.in/{CONFIG['city']}?format=%C:+%t,+%w&m"
        if CONFIG['units'] == 'imperial':
            url = f"https://wttr.in/{CONFIG['city']}?format=%C:+%t,+%w&u"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.text.strip()
        return "🌡️ Weather unavailable"
    except Exception:
        return "🌡️ No connection"

def get_system_stats():
    """Get CPU and memory usage (cross-platform)"""
    try:
        import psutil
        cpu = psutil.cpu_percent(interval=0.5)
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        return {
            "cpu": cpu,
            "memory": mem.percent,
            "disk": disk.percent,
        }
    except ImportError:
        # Fallback if psutil not installed
        return {"cpu": 0, "memory": 0, "disk": 0}

def get_quote():
    """Random motivational quote from config or API"""
    try:
        response = requests.get("https://zenquotes.io/api/random", timeout=3)
        if response.status_code == 200:
            data = response.json()
            return f"💬 {data[0]['q']} — {data[0]['a']}"
    except Exception:
        pass
    import random
    return f"💬 {random.choice(CONFIG['quotes'])}"

def get_stock_prices(symbols):
    """Fetch stock prices (free Yahoo Finance endpoint)"""
    prices = {}
    for sym in symbols:
        try:
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}"
            response = requests.get(url, timeout=3)
            if response.status_code == 200:
                data = response.json()
                price = data['chart']['result'][0]['meta']['regularMarketPrice']
                prices[sym] = f"${price:.2f}"
            else:
                prices[sym] = "N/A"
        except Exception:
            prices[sym] = "ERR"
    return prices

def get_crypto_prices(coins):
    """Fetch crypto prices via CoinGecko"""
    prices = {}
    try:
        ids = ",".join(coins)
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd"
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            data = response.json()
            for coin in coins:
                if coin in data:
                    prices[coin] = f"${data[coin]['usd']:,.0f}"
                else:
                    prices[coin] = "N/A"
        else:
            for coin in coins:
                prices[coin] = "N/A"
    except Exception:
        for coin in coins:
            prices[coin] = "ERR"
    return prices

def get_top_processes():
    """Get top 5 CPU-consuming processes (Linux/macOS/WSL)"""
    try:
        if sys.platform == "win32":
            return [("Windows", "Task Manager not supported")]
        # Use psutil for cross-platform
        import psutil
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
            try:
                cpu = proc.info['cpu_percent']
                if cpu and cpu > 0:
                    processes.append((proc.info['name'], cpu))
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        processes.sort(key=lambda x: x[1], reverse=True)
        return processes[:5]
    except:
        return [("N/A", 0)]

def get_calendar_events():
    """Simulate calendar (no API key) — replace with Google Calendar if needed"""
    now = datetime.now()
    # Fake events for demo — you can extend with `icalendar` or Google API
    fake_events = [
        "🟢 10:00 AM - Standup",
        "📝 2:00 PM - Code Review",
        "🎯 4:30 PM - Gym",
    ]
    return fake_events

def get_github_activity():
    """Fake GitHub-like activity (you can add real API later)"""
    return [
        "📦 Pushed to vibe-dashboard",
        "⭐ Starred 3 repos",
        "🐛 Closed issue #42",
    ]

# ========== UI COMPONENTS ==========
def make_layout() -> Layout:
    layout = Layout()
    layout.split_column(
        Layout(name="top", size=3),
        Layout(name="middle"),
        Layout(name="bottom", size=5),
    )
    layout["middle"].split_row(
        Layout(name="left"),
        Layout(name="right"),
    )
    return layout

def render_header() -> Panel:
    now = datetime.now().strftime("%A, %B %d, %Y • %I:%M %p")
    header_text = Text(f"✨ VIBE DASHBOARD ✨\n{now}", justify="center", style="bold cyan on black")
    return Panel(Align.center(header_text), box=box.HEAVY, border_style="cyan")

def render_weather_system() -> Panel:
    weather = get_weather()
    stats = get_system_stats()
    
    content = f"""
🌤️  Weather: {weather}

💻 System:
   • CPU:  {stats['cpu']}%
   • RAM:  {stats['memory']}%
   • Disk: {stats['disk']}%
"""
    return Panel(content.strip(), title="🌦️ Weather & System", border_style="green")

def render_stocks_crypto() -> Panel:
    stocks = get_stock_prices(CONFIG['stocks'])
    crypto = get_crypto_prices(CONFIG['crypto'])
    
    lines = ["📈 STOCKS"]
    for sym, price in stocks.items():
        lines.append(f"   {sym}: {price}")
    lines.append("\n🪙 CRYPTO")
    for coin, price in crypto.items():
        coin_emoji = "₿" if "bitcoin" in coin else "Ξ"
        lines.append(f"   {coin_emoji} {coin.title()}: {price}")
    
    return Panel("\n".join(lines), title="💰 Markets", border_style="yellow")

def render_processes() -> Panel:
    procs = get_top_processes()
    table = Table(show_header=True, header_style="bold magenta", box=box.SIMPLE)
    table.add_column("Process", width=20)
    table.add_column("CPU %", justify="right", width=8)
    
    for name, cpu in procs:
        table.add_row(name[:20], f"{cpu:.1f}%")
    
    return Panel(table, title="⚙️ Top Processes", border_style="blue")

def render_calendar() -> Panel:
    events = get_calendar_events()
    content = "\n".join(f"   {e}" for e in events)
    if not content:
        content = "   No events scheduled"
    return Panel(content, title="📅 Today's Schedule", border_style="magenta")

def render_github() -> Panel:
    activity = get_github_activity()
    content = "\n".join(f"   • {a}" for a in activity)
    return Panel(content, title="🐙 GitHub Activity", border_style="red")

def render_quote() -> Panel:
    quote = get_quote()
    return Panel(quote, title="🌟 Daily Motivation", border_style="bright_white")

# ========== MAIN LOOP ==========
def main():
    console.clear()
    console.print("[bold green]🚀 Launching Vibe Dashboard...[/bold green]")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        task = progress.add_task("Loading dashboard...", total=None)
        # Simulate loading
        import time
        time.sleep(0.5)
        progress.update(task, completed=True)
    
    layout = make_layout()
    
    with Live(layout, screen=True, refresh_per_second=4) as live:
        try:
            while True:
                # Update all panels
                layout["top"].update(render_header())
                
                left_columns = []
                right_columns = []
                
                # Left side
                layout["left"].update(
                    Layout(name="left_inner")
                )
                left_inner = layout["left"]
                left_inner.split_column(
                    Layout(name="weather_sys"),
                    Layout(name="processes"),
                )
                left_inner["weather_sys"].update(render_weather_system())
                left_inner["processes"].update(render_processes())
                
                # Right side
                layout["right"].update(
                    Layout(name="right_inner")
                )
                right_inner = layout["right"]
                right_inner.split_column(
                    Layout(name="markets"),
                    Layout(name="calendar"),
                    Layout(name="github"),
                )
                right_inner["markets"].update(render_stocks_crypto())
                right_inner["calendar"].update(render_calendar())
                right_inner["github"].update(render_github())
                
                # Bottom
                layout["bottom"].update(render_quote())
                
                # Wait before refresh
                import time
                time.sleep(CONFIG['update_interval_seconds'])
                
except KeyboardInterrupt:
    console.print("\n[bold yellow] Dashboard stopped.
Stay productive![/bold yellow]")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        console.print("[yellow]Tip: Run 'pip install rich requests python-dotenv psutil' first[/yellow]")
