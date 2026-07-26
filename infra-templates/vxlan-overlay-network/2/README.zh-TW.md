<!-- SPDX-License-Identifier: MIT -->

# PastureStack VXLAN 覆疊網路 0.3.0-rc9

此選用基礎架構範本會在受管主機間安裝未加密的 VXLAN 資料平面。
範本會公開 UDP `4789`、為每個網路持有服務執行一個路由相關容器，
並在每台符合條件的主機上安裝經審核的 CNI 執行檔。

## 已審核映像

- 映像：`ghcr.io/pasturestack/ipsec-vxlan-overlay-network:v0.14.26`
- 原始碼：
  [`PastureStack/ipsec-vxlan-overlay-network@e80db2268c9c0182b3b627e0c185998d9db91524`](https://github.com/PastureStack/ipsec-vxlan-overlay-network/tree/e80db2268c9c0182b3b627e0c185998d9db91524)
- 原始碼採 Apache-2.0 授權；Ubuntu、CNI、Weave 及隨附相依套件
  保留各自的上游授權及聲明。
- Trivy 結果為 HIGH 0、CRITICAL 0，映像機密資料與個人識別標記
  掃描均已通過。
- 隔離雙節點 VXLAN 轉送及雙向覆疊流量測試已通過。

## 安全性與網路界線

VXLAN 只封裝流量，不提供加密或身分驗證。此驅動程式只能用於受信任
的主機網路，每台參與主機都必須允許 UDP `4789` 的輸入及輸出流量。
需要主機間加密時，請改用 IPsec 加密網路範本。

路由器在網路持有服務的命名空間中使用 `NET_ADMIN`。CNI 相關容器
使用特權模式、加入主機網路與 PID 命名空間，並存取 Docker Socket
以安裝及操作相容 CNI 路徑。這些權限不得套用到一般工作負載。

受管網路為 `10.42.0.0/16`。經審核的啟動流程無法安全套用任意
子網路，因此此版本不提供無效的子網路選項。

## 相容性界線

`rancher-compose.yml`、`minimum_rancher_version`、必要的
`io.rancher.*` 編排標籤及 `rancher-cni-driver` 共用磁碟區是相容
控制平面使用的協定識別名稱，不是目前的產品品牌。使用者可見名稱、
映像位置、環境變數、CNI 名稱、日誌路徑及 `pasture.internal`
搜尋後綴均採 PastureStack 名稱。
