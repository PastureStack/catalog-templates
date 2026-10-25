<!-- SPDX-License-Identifier: MIT -->

# PastureStack 系統映像預先下載 v0.3.3 候選版

## 目前來源候選

本來源只準備數字修訂 4，尚未發布或部署。目前已發布的安裝座標仍是 Catalog v0.3.16 與數字修訂 3。新元件的 digest、producer、SBOM 與掃描收據尚待提供，因此不宣稱新成品已通過驗收；目前仍會被 image 發布證據 gate 阻擋。

預計替換的映像（已發布輸入 → 尚未發布候選）：

- `ghcr.io/pasturestack/system-image-preloader:v0.3.2` → `ghcr.io/pasturestack/system-image-preloader:v0.3.3`

除了這些映像 tag 與 Catalog 顯示版號，runtime 定義逐位元組保留原修訂。命令、預設值、資源參數、權限、附屬容器、磁碟區、防火牆選項與 plugin 職責都沿用既有契約。取得真實發布證據後才能提升本來源候選。

## 已發布修訂 3 的參考說明

以下相容性說明與驗證陳述只對應先前已發布的輸入，不能作為新候選映像的驗收證據。

此全域、只執行一次的基礎架構服務會找出相容系統堆疊使用的映像，並
要求每台主機的 Docker 常駐程式預先快取尚未存在的映像。

### 已審核映像

- 映像：`ghcr.io/pasturestack/system-image-preloader:v0.3.2`
- 原始碼：
  [`PastureStack/system-image-preloader@bcd89e7fb6baafea381de380c256e4e8d62f1df2`](https://github.com/PastureStack/system-image-preloader/tree/bcd89e7fb6baafea381de380c256e4e8d62f1df2)
- 原始碼採 Apache-2.0 授權；Ubuntu、Docker CLI、`yq`、`gomplate`
  及相依套件保留各自的上游授權及聲明。
- 完整嚴重度掃描沒有可用修補、未審核項目或機密資料；官方尚無修補的 Low/Medium 持續追蹤。
- 公開 GHCR 與未登入存取版本標籤的驗證已通過。

### 安全性界線

此服務需要以讀寫方式掛載 `/var/run/docker.sock`。Docker Socket
權限等同主機管理者權限，因此只能部署經審核的映像，並限制可編輯此
堆疊的使用者。服務會自動取得範圍受限的相容 API 登入資訊，且不會
啟用可能顯示登入資訊的 Shell 追蹤。

私有登錄登入資訊為選用功能。啟用後，選取的主機 Docker
`config.json` 會以唯讀方式掛載。特權模式預設關閉，只能在主機
安全性政策確實要求時啟用。映像拉取重試與 CPU 使用量等待都有明確
上限。

相容控制平面仍需要名為 `rancher-compose.yml` 的檔案及
`io.rancher.*` 代理程式與排程標籤。這些是協定識別名稱，不是目前
的產品品牌。

### 驗證

此版本已通過離線重試與 URL 契約測試、容器說明及版本煙霧測試、
OCI 中繼資料與授權檢查、弱點掃描，以及隔離環境端對端生命週期測試。
生命週期測試使用模擬中繼資料、環境及商店 API，並透過真正的 Docker
Socket 驗證執行環境能找出 Compose 映像及快取其語意化版本標籤。
測試只移除精確建立的資源，沒有執行大範圍清理。
