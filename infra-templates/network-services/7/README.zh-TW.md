<!-- SPDX-License-Identifier: MIT -->

# PastureStack 網路服務

第 7 版使用網路外掛管理器 `v0.8.19`，保留單一防火牆後端的選擇方式，以及相同的中繼資料服務與內部 DNS 映像；並修正發布主機連接埠與 VXLAN 並存時的雙向轉送。管理器會在修改主機防火牆規則前拒絕格式錯誤或互相衝突的網橋中繼資料，並把所有受管轉送規則限制在正確網橋。啟用 `route_localnet` 前會先阻擋來自該網橋、目的為 `127.0.0.0/8` 的流量；原始的每網橋設定會保存於 `/run`，不再需要主機連接埠時則恢復原值。選用每主機子網路時，會保留跨主機容器來源位址，並只允許已驗證的對端子網路轉送至本機子網路。映像發布來源與 digest 記錄於 `catalog-images.json`。

## 防火牆後端

`FIREWALL_BACKEND` 預設為 `auto`，依 Docker 實際防火牆驅動程式選擇單一路徑：Docker 原生 `nftables` 使用原生 nft 規則；Docker `iptables` 驅動程式則辨識哪一套前端擁有 Docker 現役 NAT 鏈。任何受支援主機（包括 Ubuntu 26.04 及更新版）都可能使用 `iptables-nft` 或 `iptables-legacy`；作業系統版本、執行檔存在或尚未載入的核心模組，均不足以決定後端。需要固定路徑時可選：

- `nftables`：Docker 原生 nftables 防火牆後端，**不是** iptables-nft 相容命令。
- `iptables-nft`：由 nf_tables 支援的 xtables 相容命令，搭配 Docker 的 iptables 防火牆驅動程式。
- `iptables-legacy`：只在現役 Docker 確實透過這套前端持有規則時選用。

選擇與 Docker 實際後端不符或無法判定時，管理器會拒絕啟動，不會自動降級、切換 Docker 後端或載入 legacy 模組。Ubuntu 26.04 及更新版若已使用 `iptables-legacy` 或 `iptables-nft`，就應維持現役 Docker 路徑；不能只因系統較新便替它切成原生 nftables。刻意遷移須另外準備主機變更、回復點及網路生命週期驗收。

主機 NAT 與主機連接埠的 `CATTLE_*` 規則鏈只由此管理器維護；三種後端的來源位址轉換規則都排除受管 overlay 子網路內的目的位址。每主機子網路還會排除其他有效主機的已驗證子網路，並加入限定來源與目的子網路的轉送例外；非現役主機不列入，現役主機若缺少標籤或子網路重疊則安全地拒絕套用。此網路只提供路由、不加密，須另行保護主機間傳輸。IPsec 主機 XFRM 路由器不得再插入補丁規則。升級時應先升級網路服務，逐台確認管理器健康，再升級相符的 IPsec 加密網路版本。

使用 Docker 原生 nftables 前，必須先在主機 Docker 設定加入 `"firewall-backend": "nftables"` 及 `"bridge-accept-fwmark": "0x1068/0x1068"`，再升級此堆疊。還須在主機持久設定 `net.ipv4.ip_forward=1`，並於重開機後確認仍啟用；Docker 原生 nftables 後端不會代為啟用 IPv4 轉送。此標記讓 Docker 網橋轉送規則接受管理器發布的主機連接埠流量；範本無法替主機設定 Docker daemon 或核心參數。切換前還須檢查並明確遷移殘留的 `iptables-nft FORWARD DROP` 全域政策與舊平台掛鉤。管理器遇到混用狀態會拒絕啟動，不會自行修改主機全域防火牆政策。Docker 原生 nftables 目前仍屬實驗性功能，正式環境使用前應針對安裝的 Docker 版本完成驗收。

## 其他設定

- `DOCKER_BRIDGE`：受管工作負載使用的主機網橋。
- `DNS_RECURSER_TIMEOUT`、`TTL`：上游 DNS 逾時與服務探索快取時間。
- `CPU_PERIOD`、`CPU_QUOTA`：中繼資料服務的 CPU 排程限制。
- `RELOAD_INTERVAL_LIMIT`、`ARP_SYNC_INTERVAL`：中繼資料重新載入與主機 ARP 協調間隔。

網路外掛管理器仍需主機網路、主機 PID、Docker Socket、Docker 狀態、核心模組與執行環境掛載，以及共用 CNI 磁碟區。中繼資料服務僅在指派連結本機位址時以 root 啟動，之後切換為 UID/GID 10001；內部 DNS 與其共用網路命名空間。`rancher-compose.yml`、`io.rancher.*`、`CATTLE_*` 備援變數、`/var/lib/rancher` CA 路徑及 `rancher-cni-driver` 磁碟區是既有協定的相容契約，不代表必須使用 legacy 防火牆規則。

範本檔案採 MIT 授權；管理器、中繼資料服務與內部 DNS 保留 Apache-2.0 授權及隨附相依套件聲明。部署前應以 `catalog-images.json` 核對映像來源與記錄的 manifest digest。
