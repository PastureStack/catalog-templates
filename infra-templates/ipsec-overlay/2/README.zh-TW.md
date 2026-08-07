<!-- SPDX-License-Identifier: MIT -->

# PastureStack IPsec 加密網路 0.3.0-rc2

此基礎架構範本會在每台符合條件的主機上安裝經審核的 IPsec 加密
網路資料平面。網路持有服務負責受管命名空間；路由器套用主機 XFRM
與路由狀態；連線檢查相關容器提供控制平面健康狀態契約；CNI 相關
容器則提供經審核的網橋與位址管理執行檔。

## 已審核映像

- 映像：`ghcr.io/pasturestack/ipsec-vxlan-overlay-network:v0.14.26`
- 原始碼：
  [`PastureStack/ipsec-vxlan-overlay-network@e80db2268c9c0182b3b627e0c185998d9db91524`](https://github.com/PastureStack/ipsec-vxlan-overlay-network/tree/e80db2268c9c0182b3b627e0c185998d9db91524)
- 原始碼採 Apache-2.0 授權；Ubuntu、strongSwan、CNI、Weave 與
  隨附相依套件保留各自的上游授權及聲明。
- Trivy 結果為 HIGH 0、CRITICAL 0，映像機密資料與個人識別標記
  掃描均已通過。
- 已通過雙主機加密 IPsec 流量、受管 CNI、中繼資料、DNS、主機
  連接埠、常駐程式復原、滾動替換、升級與回復測試。

## 權限與機密資料界線

路由器使用特權模式並加入主機 PID 與網路命名空間，會變更 XFRM、
路由、防火牆、網橋、ARP 及轉送狀態。CNI 相關容器也使用特權模式
並存取 Docker Socket。這些權限是相容架構所需，不得套用到一般
工作負載。

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

## 發布界線

映像、隔離資料平面及商店建立的雙主機測試均已通過，包括雙向 HTTP
與 ICMP、AES-GCM XFRM、服務 DNS、中繼資料、相同主機連接埠、
Docker 常駐程式重啟、滾動升級、第二次設定替換、原生回復與多輪
健康狀態穩定檢查。在完整移除基礎架構堆疊及全新多 VM 驗收完成前，
仍不得宣告正式環境核准。
