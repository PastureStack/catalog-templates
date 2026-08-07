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
