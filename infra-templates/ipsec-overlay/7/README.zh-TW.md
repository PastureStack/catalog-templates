<!-- SPDX-License-Identifier: MIT -->

# PastureStack IPsec 加密網路 0.3.5

此候選基礎架構範本預計在每台符合條件的主機上安裝 IPsec 加密
網路資料平面。網路持有服務負責受管命名空間；路由器套用主機 XFRM
與路由狀態；連線檢查相關容器提供控制平面健康狀態契約；CNI 相關
容器則提供網橋與位址管理執行檔。

## 候選範本：映像已發布

- 映像 `ghcr.io/pasturestack/ipsec-vxlan-overlay-network:v0.14.32` 已正式發布；
  真實 manifest digest、來源 revision 與執行映像安全掃描已記錄於
  `catalog-images.json`。GitHub Release 並未標示為不可變。
- 第 `7` 版保留第 `6` 版的對等主機重試與 8111 連接埠交接。
  新版讓同一對等主機的重複 IKE SA 收斂；只有健康替代 CHILD_SA
  已建立時，才清除卡在 `DELETING` 的舊 SA。歷史範本不回寫。
- 原始碼採 Apache-2.0 授權；Ubuntu、strongSwan、CNI、Weave 與
  隨附相依套件保留各自的上游授權及聲明。

## 權限與機密資料界線

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

## 發布界線

已發布的 `v0.14.32` 映像以真實 manifest digest 鎖定。原生 nftables、
iptables-nft 與 iptables-legacy 的隔離驗收必須保持通過；受管升級及
對等主機重啟還須確認暫時離線的主機不會拆掉其他健康連線、同一對等
主機收斂為一條可用 IKE SA，新路由器
仍等待 8111 埠釋放，且不越界修改網路外掛管理器的防火牆規則。
本版實機結果須另行記錄，才可宣稱整套受管生命週期完成。
