<!-- SPDX-License-Identifier: MIT -->

# PastureStack 容器定時排程 v0.6.0

此基礎架構服務會監看 Docker 容器事件，並依排程執行 `start`、
`stop` 或 `restart`。受管工作負載可使用下列標籤啟用排程：

- `cron.schedule`：必填，使用六欄式 Cron 表達式。
- `cron.action`：選填，可設為 `start`、`stop` 或 `restart`；
  預設為 `start`。
- `cron.restart_timeout`：選填，停止或重新啟動容器的逾時秒數。

## 已審核映像

- 映像：`ghcr.io/pasturestack/container-cron:v0.6.0`
- 原始碼：
  [`PastureStack/container-cron@8645472791ebbc9f78628af716e061139554fb38`](https://github.com/PastureStack/container-cron/tree/8645472791ebbc9f78628af716e061139554fb38)
- 原始碼採 Apache-2.0 授權；Ubuntu 與內含的 Go 相依套件保留各自的
  上游授權。
- Trivy 掃描結果為 HIGH 0、CRITICAL 0。
- 公開 GHCR 與未登入存取版本標籤的驗證已通過。

## 安全性界線

此服務需要以讀寫方式掛載 `/var/run/docker.sock` 才能控制容器。
Docker Socket 權限等同主機管理者權限，因此只能將此範本當成受信任
的全域基礎架構服務部署。此服務預設不要求特權模式、不公開主機連接埠，
也不接受遠端 Docker 端點。

相容控制平面仍需要名為 `rancher-compose.yml` 的檔案及
`io.rancher.*` 排程標籤。這些是相容協定識別名稱，不是目前的產品
品牌。

## 驗證

此版本已通過啟用競爭偵測的單元測試、靜態分析、映像中繼資料與授權
檢查、弱點掃描，以及 Docker 29.4 隔離環境生命週期測試。測試確認
服務能依排程啟動一個已停止的工作負載，並停止另一個執行中的工作負載；
測試資源已精確移除。

部署採用中性的容器事件模式，不依賴舊品牌的命令列參數，也不透過
中繼資料轉譯服務狀態。
