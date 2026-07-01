# 一鍵 LED 控制(全機熄 / 開白燈)

部機 = ASUS ROG STRIX X870-A,本身冇裝任何 RGB 軟件,所以要靠 **OpenRGB**(免費開源、信任度高)做引擎。ASUS 主機板 LED 一定要**一次 admin(UAC)**先郁得到,所以下面 setup 同指令都會自動彈一次 UAC。

## 用法(瞓醒做一次)
1. **入面 `setup-once.cmd` 撳兩下** → 彈 UAC 撳「是」→ 佢用 winget 裝 OpenRGB,裝完會列出偵測到嘅 LED 裝置。
   （或者開 terminal 打:`winget install OpenRGB.OpenRGB`）

## 之後日常(一個指令)
- **熄晒全機 LED**:撳兩下 `leds-off.cmd`(彈 UAC →「是」)
- **全部開返白燈**:撳兩下 `leds-white.cmd`(彈 UAC →「是」)

> 第一次 UAC 之後,如果想連 UAC 都唔彈,可叫我幫你整一個「已提權」捷徑(Task Scheduler 方式),咁就真係一個指令零彈窗。

## 老實講(make no mistakes)
- OpenRGB 會控制佢**偵測到**嘅裝置:主機板 Aura、RAM、顯卡、ARGB 風扇通常 OK。
- **鍵盤**睇型號 —— `setup-once.cmd` 列出嘅 device 清單會話你接唔接到。若鍵盤唔喺清單,佢自己通常有 `Fn + 燈光鍵` 可手動熄。
- 「熄」= 將所有 LED 設成黑色(等於熄);個別裝置若仍微亮,話我知我再幫佢加 profile。
- 全部本機操作、可還原;OpenRGB 經 winget 官方來源安裝。

— Claude 整定(2026-06-30)。你瞓醒試,有問題嗌我。
