<!-- SPDX-License-Identifier: MIT -->

# 舊版 Container Crontab 升級至 Container Cron v0.6.2

此相容項目不列於新建目錄；新建安裝仍使用
`pasturestack:infra*container-schedule:4`。
既有 `catalog://library:infra*container-crontab:3` 透過唯讀相容解析，
使用正常 Stack `upgrade`、`finishupgrade` 與 `rollback` 動作升級。
僅讀取相容識別碼不會改動 Stack。

第 3 版保留自官方
[`rancher/rancher-catalog@52a5850bc49247eadd84045da890deaeaeddb9a4`](https://github.com/rancher/rancher-catalog/tree/52a5850bc49247eadd84045da890deaeaeddb9a4/infra-templates/container-crontab/3)。
其 `rancher/container-crontab:v0.5.0` 僅供歷史版本讀回與升級回復，
未重新驗證現行安全狀態，也不宣稱通過目前安全閘門。

第 4 版使用已發布的 `ghcr.io/pasturestack/container-cron:v0.6.2`，
來源、映像摘要、SBOM 與掃描證據均沿用 `catalog-images.json` 的既有紀錄。
服務名稱維持 `container-crontab`，問題變數維持 `metrics`、`debug`，
避免新增第二套排程服務或重設原有答案。正式升級讓識別碼在原命名空間
由 `:3` 前進至 `:4`，不直接改寫命名空間或資料庫。

新版本保留全主機部署、Docker socket 掛載、持續重新啟動與容器名稱主機名稱。
舊版 `--rancher-mode` 正式對應至維護版的 `--metadata-mode`，保留中繼資料
服務狀態檢查：受管工作負載僅在服務為 `active` 時執行排程，服務停用或
等待升級確認時暫停排程。過時 Docker API 覆寫仍移除。
工作負載本身的 `cron.schedule`、
`cron.action`、`cron.restart_timeout`、時區標籤、`TZ` 環境值與其他選項
必須維持原值；此版本未新增 `cron.timezone` 的解讀功能。

`upgrade_strategy.start_first: false` 明確要求每台主機先停止舊排程容器，
再啟動替代容器；回復也使用相同服務升級策略。執行程式沒有跨程序選主，
不可在同一 Docker daemon 另行啟動 canonical Container Schedule。

升級確認前，讀回相同 Stack 與服務識別碼、原有 `metrics`／`debug` 答案、
工作負載標籤與選項，並由 Docker 事件確認新舊容器沒有重疊執行。
先驗證正常 rollback，再執行 `finishupgrade` 結束原生回復視窗；
新映像無法啟動時，也必須能使用正常 Stack rollback 回復。
