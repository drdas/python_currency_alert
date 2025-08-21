# 💱 Currency Alert App (Windows Tray)

[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![License:
MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows-0078D6?logo=windows)](https://www.microsoft.com/windows)
[![Dependencies](https://img.shields.io/badge/dependencies-pip-blue)](requirements.txt)

A simple Windows tray application that monitors foreign exchange (FX)
rates using [Alpha Vantage](https://www.alphavantage.co/) and alerts you
when they move outside your defined thresholds.

The app runs in the background, shows live rate updates in the system
tray, and provides toast notifications when the currency pair moves
beyond your set range.

------------------------------------------------------------------------

## ✨ Features

-   🔔 **Real-time FX alerts** with toast notifications
-   🟦🔴 **Tray icon color change** based on status (`OK` = blue,
    `ALERT` = red)
-   ⚙️ **Configurable settings** (currencies, thresholds, refresh
    interval) via GUI
-   🛑 **Prevents multiple instances** with a mutex lock
-   💾 **Settings saved** to `config.json`
-   🪟 Designed for **Windows 10/11** system tray

------------------------------------------------------------------------

## 📦 Requirements

Install dependencies manually:

``` bash
pip install requests pystray pillow schedule win10toast-click pywin32
```

or using requirements:

``` bash
git clone https://github.com/your-username/currency-alert-app.git
cd currency-alert-app
pip install -r requirements.txt
```

------------------------------------------------------------------------

## ⚡ Usage

1.  Get a free API key from [Alpha
    Vantage](https://www.alphavantage.co/support/#api-key).\

2.  Open `currency_alert_app_hourly_no_api_key.py` in an editor.

    -   Replace the placeholder:

        ``` python
        api_key = "GET_API_KEY_FROM_PROVIDER"
        ```

3.  Run the app:

    ``` bash
    python currency_alert_app_hourly_no_api_key.py
    ```

4.  The tray icon will appear (blue = OK, red = alert).

------------------------------------------------------------------------

## ⚙️ Settings

You can configure:\
- **Base / Target currency** (e.g., USD → JPY)\
- **Low / High alert thresholds**\
- **Refresh interval (minutes)**

### Methods

-   Right-click the tray icon → **Settings**\

-   Or edit `config.json` directly:

    ``` json
    {
      "pair": ["USD", "JPY"],
      "low": 140.0,
      "high": 160.0,
      "interval": 15
    }
    ```

------------------------------------------------------------------------

## 🖥️ Example

-   Watching **USD → JPY**\
-   Interval = 15 minutes\
-   Alert when rate falls below `140.0` or rises above `160.0`.

Tray icon changes color and shows a toast:

    FX Alert: USD→JPY
    Rate 161.23 outside 140.0–160.0

------------------------------------------------------------------------

## 🚀 Future Improvements

-   Cross-platform support (Linux/Mac)\
-   Multiple pairs monitoring\
-   Graphical chart view of recent rates

------------------------------------------------------------------------

## 📜 License

MIT License -- feel free to modify and use.
