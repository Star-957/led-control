# Windows RGB 控制：OpenRGB 熄燈／白燈與聯力 LCD 報告

呢個 repo 包含舊版 OpenRGB 主機板燈光腳本，以及 **Lian Li TL Wireless LCD 風扇、L-Connect 3 與 8.8 吋螢幕背光控制**技術報告。

[English README](README.md) · [聯力 LCD 控制報告](docs/lian-li-tl-wireless-lcd-lighting.md)

## 先分清控制範圍

- `leds-off.cmd` / `leds-white.cmd`：呼叫 Python 經本機 OpenRGB SDK，優先控制主機板；搵唔到主機板時會改為所有偵測裝置。唔會控制 LCD 圖像或聯力專用 LCD 背光。
- `setup-once.cmd`：要求 UAC，OpenRGB 缺少時嘗試用 winget 安裝，再列出裝置；winget 參數會自動接受套件／來源協議，執行前先閱讀條款，或自行安裝 OpenRGB。唔會安裝 Python package 或明確啟用 SDK server；要另外設定。
- 聯力報告：記錄另一份已實機測試嘅本機 adapter、指令欄位陷阱同驗證界線。個人裝置識別碼、設定備份、廠商程式同該機專用 adapter 冇包括喺公開 repo。

## 舊腳本要求與限制

需要 Windows、運行中嘅 OpenRGB SDK server（127.0.0.1:6742）及 Python 3 + `openrgb-python`。兩個日常 cmd 本身唔會提權；只有 setup 有 UAC 流程。

舊 Python 腳本會嘗試 Direct mode，並向可調燈區要求 120 粒 LED。固定值未按每款硬件核對；先備份 profile、確認真實 LED 數量，唔好假設 SDK 必定安全限制數值。錯誤可能被捕捉後繼續，所以顯示 Done 或 exit code 0 唔等於全部成功。本次公開更新係文件同報告，唔係對所有硬件作兼容認證，亦未重新實機測試呢兩個舊 Python 腳本。

「熄燈」係要求黑色／零背光，唔係停風扇或切斷 LCD 電源。圖片保留、LED 白光、散熱設定不變，要分開驗證。重開機後持續效果亦需另外測試。

## 私隱與授權

燈光控制走 localhost；安裝套件需要網絡。唔好公開裝置序號、個人設定、登入資料、API keys 或完整應用程式備份。保留正常 UAC，唔建議繞過權限檢查。

[MIT 授權](LICENSE)。不重新分發廠商程式、反編譯原始碼或 LCD 圖像。
