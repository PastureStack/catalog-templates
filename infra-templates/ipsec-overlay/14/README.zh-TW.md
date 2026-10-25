<!-- SPDX-License-Identifier: MIT -->

# PastureStack IPsec 加密網路 v0.3.12 候選版

## 目前來源候選

本來源只準備數字修訂 14，尚未發布或部署。目前已發布的安裝座標仍是 Catalog v0.3.16 與數字修訂 13。新元件的 digest、producer、SBOM 與掃描收據尚待提供，因此不宣稱新成品已通過驗收；目前仍會被 image 發布證據 gate 阻擋。

預計替換的映像（已發布輸入 → 尚未發布候選）：

- `ghcr.io/pasturestack/ipsec-vxlan-overlay-network:v0.14.40` → `ghcr.io/pasturestack/ipsec-vxlan-overlay-network:v0.14.41`

除了這些映像 tag 與 Catalog 顯示版號，runtime 定義逐位元組保留原修訂。命令、預設值、資源參數、權限、附屬容器、磁碟區、防火牆選項與 plugin 職責都沿用既有契約。取得真實發布證據後才能提升本來源候選。

## 已發布修訂 13 的參考說明

以下相容性說明與驗證陳述只對應先前已發布的輸入，不能作為新候選映像的驗收證據。

此基礎架構範本會在每台符合條件的主機上安裝 IPsec 加密
網路資料平面。網路持有服務負責受管命名空間；路由器套用主機 XFRM
與路由狀態；連線檢查相關容器提供控制平面健康狀態契約；CNI 相關
容器則提供網橋與位址管理執行檔。

### 正式發布映像

- [映像 `ghcr.io/pasturestack/ipsec-vxlan-overlay-network:v0.14.40`](https://github.com/PastureStack/ipsec-vxlan-overlay-network/releases/tag/v0.14.40)。
- [來源 `4711833178a05e5d225e364cce856bd108bdc707`](https://github.com/PastureStack/ipsec-vxlan-overlay-network/tree/4711833178a05e5d225e364cce856bd108bdc707)，簽署版本標籤已驗證。
- 第 13 版保留第 12 版的命名空間、相關容器、XFRM、防火牆選擇與 CNI 責任；既有數字版目錄內容不變。
- 完整執行映像掃描沒有可用修補、High/Critical、未知嚴重度或機密資料；54 筆官方尚無修補的 Low/Medium 持續追蹤，不視為已解決。SBOM、摘要與報告記錄於 `catalog-images.json`。
- 原始碼採 Apache-2.0 授權；隨附相依套件保留各自的上游授權及聲明。

### 權限與機密資料界線

路由器使用特權模式並加入主機 PID 與網路命名空間。在三種防火牆
後端，它只同步 IPsec XFRM 狀態與路由，不寫入主機防火牆規則。
網路外掛管理器獨自維護 overlay 網橋子網路的轉送標記、NAT 排除及
主機連接埠規則。路由器不另建 nftables 標記表、不修改管理器的
`CATTLE_*` 規則鏈，也不修改 Docker 的規則表。路由器以唯讀掛載 Docker Socket 查詢
實際防火牆驅動程式；唯讀掛載仍賦予強大的 Docker API 存取能力，
只限此受信任的特權系統服務使用。CNI 相關容器也存取 Docker Socket。
這些權限是相容架構所需，
不得套用到一般工作負載。

路由器會從相容控制平面取得範圍受限的代理程式登入資訊，再透過已驗證
的 `configcontent/psk` 契約下載 IPsec 預先共用金鑰。此範本不接受
使用者提供的金鑰，也不會把金鑰放入公開商店、Compose 變數、映像或
日誌。

### 相容性界線

`rancher-compose.yml`、`minimum_rancher_version`、必要的
`io.rancher.*` 編排標籤、`rancher-cni-driver` 共用磁碟區及
`ipsec` 代理程式服務標記是相容控制平面與網路外掛管理器使用的協定
識別名稱。使用者可見名稱、映像位置、命令、環境變數、CNI 名稱、
日誌路徑及 `pasture.internal` 搜尋後綴均採用 PastureStack 名稱。

資料平面目前支援 `10.42.0.0/16` 相容網路。執行環境無法安全套用
任意子網路，因此範本不提供無效的子網路選項。
明確的 `allowSharedSubnetIngress` 契約只由網路外掛管理器處理；IPsec
路由器仍只負責 XFRM 與路由，不寫入主機防火牆規則。

主機防火牆後端可選 `auto`、原生 `nftables`、`iptables-nft` 或
`iptables-legacy`。選擇會透過 `PASTURESTACK_FIREWALL_BACKEND` 傳給
`overlay-router`。路由器檢查 Docker 實際驅動程式與現役規則擁有者，
不以 Ubuntu 版本推斷；Ubuntu 26.04 及更新版若已使用 `iptables-legacy`
或 `iptables-nft`，仍維持該現役路徑。明確指定與實際後端不符或狀態
無法判定時安全停止，不切換後端，也不載入尚未啟用的 legacy 模組。
同環境的 Network Services 範本應使用一致的選項。

Native 專案定義將 Network Services 排在 IPsec 前面，但清單順序
本身不保證健康狀態相依。建立或升級加密網路前，應先套用相符版本
的 Network Services，等待每台目標主機上的網路外掛管理器恢復
健康。使用原生 `nftables` 時，須先完成該範本列出的 Docker
防火牆後端、`bridge-accept-fwmark` 與持久 IPv4 轉送前置設定；
只有 IPsec 路由器無法提供管理器負責的轉送及 NAT 規則。

### 部署界線

正式執行映像與 Catalog 驗證不同於受管部署驗收。套用既有環境前，須於隔離主機驗證所選防火牆後端、對端重啟、升級及回復。單純完成 CNI 位址分配不能代替加密跨主機生命週期驗收。
