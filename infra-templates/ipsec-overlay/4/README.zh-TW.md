<!-- SPDX-License-Identifier: MIT -->

# PastureStack IPsec 加密網路 0.3.2（範本待發布）

此候選基礎架構範本預計在每台符合條件的主機上安裝 IPsec 加密
網路資料平面。網路持有服務負責受管命名空間；路由器套用主機 XFRM
與路由狀態；連線檢查相關容器提供控制平面健康狀態契約；CNI 相關
容器則提供網橋與位址管理執行檔。

## 候選範本：映像已發布

- 映像 `ghcr.io/pasturestack/ipsec-vxlan-overlay-network:v0.14.27` 已正式發布；
  不可變 manifest digest、來源 revision 與執行映像安全掃描已記錄於
  `catalog-images.json`。商店範本與各後端的主機生命週期驗收仍待完成，
  目前不得部署此候選版。
- 第 `3` 版 `v0.14.26` 的驗收證據只適用於歷史版，不能替代新版驗收。
- 原始碼採 Apache-2.0 授權；Ubuntu、strongSwan、CNI、Weave 與
  隨附相依套件保留各自的上游授權及聲明。

## 權限與機密資料界線

路由器使用特權模式並加入主機 PID 與網路命名空間。在原生
`nftables` 模式下，路由器只同步 XFRM 與路由；網路外掛管理器以
自己的主機規則負責 overlay 網橋子網路的轉送標記及 NAT 排除。
路由器不另建 nftables 標記表，也不修改 Docker 的規則表。明確
選用的 `iptables-nft` 與 `iptables-legacy` 各保留自己的 xtables
路徑，不與原生 nftables 混用。CNI 相關容器
也使用特權模式並存取 Docker Socket。這些權限是相容架構所需，
不得套用到一般工作負載。

路由器會從相容控制平面取得範圍受限的代理程式登入資訊，再透過已驗證
的 `configcontent/psk` 契約下載 IPsec 預先共用金鑰。此範本不接受
使用者提供的金鑰，也不會把金鑰放入公開商店、Compose 變數、映像或
日誌。

## 相容性界線

`rancher-compose.yml`、`minimum_rancher_version`、必要的
`io.rancher.*` 編排標籤、`rancher-cni-driver` 共用磁碟區及
`ipsec` 代理程式服務標記是相容控制平面與網路外掛管理器使用的協定
識別名稱。使用者可見名稱、映像位置、命令、環境變數、CNI 名稱、
日誌路徑及 `pasture.internal` 搜尋後綴均採用 PastureStack 名稱。

資料平面目前支援 `10.42.0.0/16` 相容網路。執行環境無法安全套用
任意子網路，因此範本不提供無效的子網路選項。

主機防火牆後端可選 `auto`、原生 `nftables`、`iptables-nft` 或
`iptables-legacy`。選擇會透過 `PASTURESTACK_FIREWALL_BACKEND` 傳給
`overlay-router`。明確指定的後端與主機不符時應安全停止；現代後端
不得自動降級至 legacy。僅在明確配置的舊主機使用 legacy，並與
同環境的 Network Services 範本選項保持一致。

Native 專案定義將 Network Services 排在 IPsec 前面，但清單順序
本身不保證健康狀態相依。建立或升級加密網路前，應先套用相符版本
的 Network Services，等待每台目標主機上的網路外掛管理器恢復
健康。使用原生 `nftables` 時，須先完成該範本列出的 Docker
防火牆後端、`bridge-accept-fwmark` 與持久 IPv4 轉送前置設定；
只有 IPsec 路由器無法提供管理器負責的轉送及 NAT 規則。

## 發布界線

`v0.14.27` 映像已正式發布，並以真實 manifest digest 鎖定。升格商店
候選版前，仍須通過商店稽核，並依後端選項驗收現代 nft-only 與明確
選用 legacy 的主機。先前
`v0.14.26` 的雙主機及滾動升級結果只適用於第 `3` 版，不能視為本版
證據。
