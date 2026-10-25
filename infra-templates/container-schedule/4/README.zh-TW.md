<!-- SPDX-License-Identifier: MIT -->

# PastureStack 容器定時排程 v0.6.2 候選版

## 目前來源候選

本來源只準備數字修訂 4，尚未發布或部署。目前已發布的安裝座標仍是 Catalog v0.3.16 與數字修訂 3。新元件的 digest、producer、SBOM 與掃描收據尚待提供，因此不宣稱新成品已通過驗收；目前仍會被 image 發布證據 gate 阻擋。

預計替換的映像（已發布輸入 → 尚未發布候選）：

- `ghcr.io/pasturestack/container-cron:v0.6.1` → `ghcr.io/pasturestack/container-cron:v0.6.2`

除了這些映像 tag 與 Catalog 顯示版號，runtime 定義逐位元組保留原修訂。命令、預設值、資源參數、權限、附屬容器、磁碟區、防火牆選項與 plugin 職責都沿用既有契約。取得真實發布證據後才能提升本來源候選。

## 已發布修訂 3 的參考說明

以下相容性說明與驗證陳述只對應先前已發布的輸入，不能作為新候選映像的驗收證據。

此基礎架構服務會監看 Docker 容器事件，並依排程執行 `start`、
`stop` 或 `restart`。受管工作負載可使用下列標籤啟用排程：

- `cron.schedule`：必填，使用六欄式 Cron 表達式。
- `cron.action`：選填，可設為 `start`、`stop` 或 `restart`；
  預設為 `start`。
- `cron.restart_timeout`：選填，停止或重新啟動容器的逾時秒數。

### 已審核映像

- 映像：`ghcr.io/pasturestack/container-cron:v0.6.1`
- 原始碼：
  [`PastureStack/container-cron@2cce2cc80f2590239d5ef758a21c54a3f1e0f2b9`](https://github.com/PastureStack/container-cron/tree/2cce2cc80f2590239d5ef758a21c54a3f1e0f2b9)
- 原始碼採 Apache-2.0 授權；Ubuntu 與內含的 Go 相依套件保留各自的
  上游授權。
- Trivy 掃描結果為 HIGH 0、CRITICAL 0。
- 公開 GHCR 與未登入存取版本標籤的驗證已通過。

### 安全性界線

此服務需要以讀寫方式掛載 `/var/run/docker.sock` 才能控制容器。
Docker Socket 權限等同主機管理者權限，因此只能將此範本當成受信任
的全域基礎架構服務部署。此服務預設不要求特權模式、不公開主機連接埠，
也不接受遠端 Docker 端點。

相容控制平面仍需要名為 `rancher-compose.yml` 的檔案及
`io.rancher.*` 排程標籤。這些是相容協定識別名稱，不是目前的產品
品牌。

### 驗證

此版本已通過啟用競爭偵測的單元測試、靜態分析、映像中繼資料與授權
檢查、弱點掃描，以及 Docker 隔離環境生命週期測試。測試確認
服務能依排程啟動一個已停止的工作負載，並停止另一個執行中的工作負載；
測試資源已精確移除。

部署採用中性的容器事件模式，不依賴舊品牌的命令列參數，也不透過
中繼資料轉譯服務狀態。
