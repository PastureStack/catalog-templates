<!-- SPDX-License-Identifier: MIT -->

# PastureStack IPsec 加密網路 0.3.10

此候選基礎架構範本預計在每台符合條件的主機上安裝 IPsec 加密
網路資料平面。網路持有服務負責受管命名空間；路由器套用主機 XFRM
與路由狀態；連線檢查相關容器提供控制平面健康狀態契約；CNI 相關
容器則提供網橋與位址管理執行檔。

## 候選範本：映像已發布

- [映像 `ghcr.io/pasturestack/ipsec-vxlan-overlay-network:v0.14.38`](https://github.com/PastureStack/ipsec-vxlan-overlay-network/releases/tag/v0.14.38)
  已於 2026-10-05 完成公開發布讀回。真實 manifest digest 為
  `sha256:5b29e08dca8a92fc0ecc7f9d0fdae0457b89daa9d02b1c1c3257bc9dd617c3ae`，
  僅作為 `catalog-images.json` 中的驗證證據，不加入部署映像引用。
- [來源 `c143e9a5f21ba6df2d1c5002340c71777f875c89`](https://github.com/PastureStack/ipsec-vxlan-overlay-network/tree/c143e9a5f21ba6df2d1c5002340c71777f875c89)
  的 commit 簽章已驗證；Git tag `v0.14.38` 為 annotated tag，但未簽章。
- 第 `12` 版將四個服務更新至已發布的 `v0.14.38` 映像，完整保留
  第 `11` 版的命名空間、相關容器、XFRM、防火牆選擇與 CNI 責任契約。
  第 `11` 版及其原有 `v0.14.35` inventory 仍供既有堆疊使用。
- 第 `11` 版為固定的 `10.42.0.0/16` CNI 網路明確設定
  `allowSharedSubnetIngress: true`。網路外掛管理器 `v0.8.20` 依此契約
  恢復跨主機工作負載轉送，且不放行設定子網路或受管網橋以外的流量。
  第 `10` 版仍供既有堆疊使用。
- 第 `10` 版在滾動升級時，若舊版連線檢查容器尚占用 TCP 80，
  新版只對此埠占用情況等待，最多 90 秒；其他監聽錯誤或逾時仍會
  明確失敗。此處不更動防火牆規則或路由器的 8111 連接埠責任。
  第 `9` 版仍供既有堆疊使用。
- 第 `8` 版保留對等主機重試與 8111 連接埠交接。IPsec 模組統一負責
  缺失 SA 的重建；超過觀察期間且同一對等主機恰有一條已使用的健康
  SA 時，才清除另一條零流量的重複 SA。無法明確判斷的連線不動。
  第 `7` 版仍供既有堆疊參照，但真機滾動升級後曾留下兩條已建立 SA。
- 第 `9` 版將隨附 CNI 的主機標籤查詢改為控制平面實際提供的純文字
  `/self/host/labels/<key>` 契約，讓每主機子網路可正確取得網橋與 IPAM
  位址範圍。第 `8` 版仍供既有堆疊使用。
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

## 發布界線

公開讀回已確認 `v0.14.38` 映像的 manifest、config、版本與來源標籤，
以及 linux/amd64 執行映像掃描的 HIGH、CRITICAL 與 secrets 均為零。
這只代表執行映像的結果，不是零 CVE 或建置映像無風險的宣告。
第 `12` 版 Catalog 範本仍為候選；精確來源的 Catalog 驗證及 API
版本查詢是分開的驗收關卡，尚未宣告 QA 部署或完整防火牆模式／外掛矩陣通過。
原生 nftables、iptables-nft 與 iptables-legacy 的隔離檢查、受管升級、
對等主機重啟及回復須另行驗收。仍須確認暫時離線的主機不拆掉其他
健康連線、同一對等主機收斂為一條可用 IKE SA、新路由器等待 8111
埠釋放，且不越界修改網路外掛管理器的防火牆規則。
單純完成 CNI 位址分配不能代替加密跨主機生命週期驗收。
