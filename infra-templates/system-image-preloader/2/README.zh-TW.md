<!-- SPDX-License-Identifier: MIT -->

# PastureStack 系統映像預先下載 v0.3.0

此全域、只執行一次的基礎架構服務會找出相容系統堆疊使用的映像，並
要求每台主機的 Docker 常駐程式預先快取尚未存在的映像。

## 已審核映像

- 映像：`ghcr.io/pasturestack/system-image-preloader:v0.3.0`
- 原始碼：
  [`PastureStack/system-image-preloader@150c78dbdb3f487a7003c83339cca5b76dde97f4`](https://github.com/PastureStack/system-image-preloader/tree/150c78dbdb3f487a7003c83339cca5b76dde97f4)
- 原始碼採 Apache-2.0 授權；Ubuntu、Docker CLI、`yq`、`gomplate`
  及相依套件保留各自的上游授權及聲明。
- Trivy 掃描結果為 HIGH 0、CRITICAL 0。
- 公開 GHCR 與未登入存取版本標籤的驗證已通過。

## 安全性界線

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

## 驗證

此版本已通過離線重試與 URL 契約測試、容器說明及版本煙霧測試、
OCI 中繼資料與授權檢查、弱點掃描，以及隔離環境端對端生命週期測試。
生命週期測試使用模擬中繼資料、環境及商店 API，並透過真正的 Docker
Socket 驗證執行環境能找出 Compose 映像及快取其語意化版本標籤。
測試只移除精確建立的資源，沒有執行大範圍清理。
