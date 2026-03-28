# Development Log (開發日誌)

## 專案規劃 (Phase 1: Planning)
- **目標**：完成 AIoT HW1 要求，包含真實與模擬兩部分的數據傳輸，並提供 Dashboard 與 Live Demo。
- **架構設計**：
  - **後端 API**：使用 Flask 接收 HTTP POST 並將感測資料寫入 SQLite 資料庫 (`aiotdb.db`)。
  - **前端儀表板**：使用 Streamlit 讀取 SQLite 產生即時資料表與圖表。
  - **感測端 (模擬)**：撰寫 Python 腳本 (`esp32_sim.py`) 隨機產生假溫濕度數據來模擬物聯網裝置行為。
  - **感測端 (真實)**：撰寫 Arduino C++ 程式 (`esp32_real.ino`)，提供給真正的 ESP32 與 DHT11 模組燒錄與上傳真實環境資料。

## 系統實作 (Phase 2: Implementation)
1. **資料庫與 API 建立 (`app.py`)**：使用 Flask 建立 `/sensor` API，並在啟動時自動初始化 SQLite 資料表，完成測試確認 `201 Created` 成功接收與紀錄資料。
2. **模擬器開發 (`esp32_sim.py`)**：使用 `requests` 模組，設定每 5 秒送出 JSON 格式數據打到 Flask API 上。
3. **介面開發 (`streamlit_app.py`)**：利用 `pandas` 查詢資料庫，並使用 `st.metric`, `st.line_chart` 自動抓取更新資料呈現。
4. **真實設備程式碼 (`esp32_real.ino`)**：建立真實世界硬體開發所需的 C++ 程式碼。

## 本機測試與除錯 (Phase 3: Testing)
- **虛擬環境建立與除錯**：在開發初期遇到 Windows PowerShell 的 `Execution_Policies` 權限問題，改以指定 `venv\Scripts\python.exe` 絕對路徑的方式成功安裝依賴套件與繞過限制。
- **驗證**：系統整合測試成功，`esp32_sim.py` 將超過 200 筆假資料成功寫入了 `aiotdb.db` 中，且 `streamlit_app.py` 成功以圖表視覺化。

## 部署與交付 (Phase 4: Deployment)
- 初始化 Git，排除 `venv/` 中繼資料，包含所需的 `README.md` 等作業規定文件。
- **Live Demo 規劃**：基於作業需求，我們決定維持輕量化的 `SQLite`。在將專案推送至 GitHub 後，會由 Streamlit Community Cloud 直接讀取夾帶上傳的 `aiotdb.db` 檔案來當作雲端展示的 Live Demo。
