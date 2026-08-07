# PastureStack Kubernetes 叢集

PastureStack 是獨立的社群計畫，目的在保存、稽核與現代化 Rancher
1.6 生態系；本計畫與 Rancher Labs 或 SUSE 無隸屬或背書關係。

此商店範本使用持續維護的 PastureStack 執行映像部署 Kubernetes
1.12.10 相容叢集。它衍生自上游 `rancher/catalog` Kubernetes
範本第 63 版；儲存庫保留上游 Git 歷史、作者、日期、授權與出處。

## 內含執行元件

- Kubernetes 1.12.10 相容套件
- 具有 TLS 與備份功能的 etcd 2.3.7 相容服務
- kubectl 服務及互動式命令列
- 主機檔案更新程式
- 控制平面整合代理程式
- 身分驗證 Webhook 橋接器
- 入口流量負載平衡服務
- 專用 Pod 暫停容器與資料磁碟區輔助映像

所有使用者可見的映像都使用語意化版本標籤。不可變更的摘要、SBOM、
弱點掃描與整合測試證據保留在商店介面以外。

## 相容更新第 5 版

本版只將 etcd 服務映像更新為
`etcd-compat:v2.3.7-pasturestack.2`。此相容版本以會驗證受管服務身分的
雙向 TLS 取代寬鬆的健康檢查 TLS、修正在 Go 1.26 上使用 Unix Socket
的 v3 用戶端端點，並以固定格式處理 gRPC 錯誤訊息。公開映像的 Trivy
掃描為 Critical 0、High 0，映像機密掃描為 0；CycloneDX SBOM 共列出
130 個元件。商店範本第 4 版維持位元組完全不變，供管理者比對定義或
回復使用。

這項安全性更新不會變更既有 etcd 資料格式，也不代表 etcd 2.3 重新
獲得上游支援。升級現有控制平面堆疊前，請先建立備份並實際驗證還原
流程。

## 相容更新第 4 版

本版維持所有控制平面服務使用已審核的
`kubernetes-package:v1.12.10-pasturestack.3`，並將兩個商店操作服務
更新為 `kubectl-service:v0.9.11-pasturestack.5`。新版 kubectl 服務只
允許連線到核准的內部 Kubernetes API 端點、拒絕重新導向與不安全的
命名空間值，也不會把未受信任的請求資料寫入作業日誌。CodeQL 找出的
請求偽造與日誌注入問題均已由程式碼修正，沒有使用忽略或解除方式；
公開映像的 Trivy 掃描為 Critical 0、High 0，映像機密掃描為 0。
相對應的套件版本繼續使用已審核的
`tiller:v2.17.0-pasturestack.2` 相容映像，並在滾動更新前後核對全部
Helm 2 發行紀錄。上一版範本固定保留為第 3 版，方便管理者比對或回復
商店定義。

這次更新修正過時映像與發行版本對照不一致的問題，但不代表
Kubernetes 1.12、etcd 2.3 或 Helm 2 重新獲得上游支援。此範本只能
作為隔離的匯入與移轉邊界；請保留 etcd 與 Helm 發行資料備份，並依
元件儲存庫中的分階段退場程序處理。

## 刻意排除的舊版附加元件

歷史範本可安裝 Dashboard、KubeDNS、Heapster、Grafana、InfluxDB
及 Tiller。這些選用第三方映像不會複製到 PastureStack：其中數個
含有 Critical 等級弱點，而且已停止維護的專案不在本次第一方平台
移植範圍內。因此範本不會提供可能建立不安全或故障部署的附加元件
開關。

核心叢集可用於 API、排程、服務網路、身分驗證、入口流量、備份及
Pod 沙箱相容性測試。正式使用叢集 DNS 與監控前，仍需另行提供經
審核的元件。

## 必要主機連接埠

請開放 TCP `10250` 與 `10255` 供 kubectl 存取。NodePort 服務
預設使用 TCP `30000` 到 `32767`。

## 平面隔離

預設的 `none` 模式適合精簡概念驗證。若要採用正式環境式分離，
請選擇 `required`，並分別為主機設定 `compute=true`、
`orchestration=true` 與 `etcd=true` 標籤。

## 升級安全

請勿將早於 `v1.2.4-rancher9` 的歷史叢集直接升級到此版本。必須先
經過歷史 `v1.5.4-rancher1` 界線，並先建立 etcd 備份。變更正式
堆疊前應先驗證備份能否還原。

## 相容協定識別名稱

範本保留有限的 `io.rancher.*` 標籤、`minimum_rancher_version`、
內部 `.rancher.internal` DNS 名稱、供應商值及控制器環境變數。
這些是 Cattle 1.6 API 必要的協定識別名稱，不是目前的產品品牌。
服務名稱與使用者可見說明均採 PastureStack 用語。

範本採 Apache License 2.0 授權。每個引用映像與隨附套件保留各自
的授權及出處聲明。
