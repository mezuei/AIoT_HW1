# AIoT System HW1

此專案為基礎的 AIoT 系統，包含「真實設備」及「電腦軟體模擬」兩個部分，串接感測器、網頁伺服器 API 與前端視覺化儀表板。

## 目錄結構
- `app.py`: Flask 伺服器，負責提供 API 並將數據存入 SQLite。
- `esp32_sim.py`: **模擬端**的 Python 腳本，模擬發送設備數據。
- `esp32_real/esp32_real.ino`: **真實端**的 Arduino 程式碼 (給實體 ESP32 + DHT11 燒錄使用)。
- `streamlit_app.py`: Streamlit 儀表板，讀取資料庫並繪製圖表。
- `requirements.txt`: 專案所需的套件。
- `aiotdb.db`: Local 端測試時收集的 SQLite 數據庫。
- `DEV_LOG.md`: 開發過程日誌。

## 本機執行說明 (Local)
1. 安裝依賴：`pip install -r requirements.txt`
2. 啟動 Flask 伺服器：`python app.py` (伺服器將執行於 port 5000)
3. 啟動模擬感測端：`python esp32_sim.py`
4. 啟動 Streamlit 儀表板視覺化介面：`streamlit run streamlit_app.py`

## 真實設備使用說明 (ESP32)
1. 以 Arduino IDE 開啟 `esp32_real/esp32_real.ino`。
2. 修改 `ssid` 與 `password` 為您的 Wi-Fi 資訊。
3. 修改 `serverName` 為您運行 `app.py` 電腦的 **區網 IP**。
4. 燒錄進入 ESP32，並請將真實的 DHT11 模組資料腳位接至 ESP32 的 Pin 4。

## Live Demo 架構 (部署至 Streamlit)
本專案的 Demo 可藉由 [Streamlit Community Cloud](https://share.streamlit.io/) 直接建立。
1. 將本資料夾所有檔案推送到 GitHub Repository。
2. 前往 Streamlit Cloud，建立新 App 並連接該 GitHub Repository。
3. Entrypoint 填寫 `streamlit_app.py` 並直接部署，系統便會讀取專案內的 `aiotdb.db` 展示靜態歷史紀錄作為 Live Demo。
