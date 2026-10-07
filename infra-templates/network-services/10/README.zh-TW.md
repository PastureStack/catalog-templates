<!-- SPDX-License-Identifier: MIT -->

# PastureStack 網路服務

第 10 版（顯示版本 `v0.3.8`）使用已正式發布的網路外掛管理器 `v0.8.22`，修正從歷史執行環境升級時的 CNI 設定收斂。單一防火牆後端的選擇方式、中繼資料服務 `v0.9.11`、內部 DNS `v0.17.11`、所有 Catalog 問題，以及第 9 版的轉送與主機連接埠契約均維持原樣；第 9 版保留不可變的原始內容。官方映像來源、manifest digest 與實際執行環境掃描證據記錄於 `catalog-images.json`。

## CNI 設定收斂

管理器會先檢查所有預期 CNI 設定，再以原子置換逐檔寫入，權限為 `0600`。只有全部預期設定都寫入成功後，才可退役已不再使用的平台設定。歷史 `10-rancher.conf` 的 name/type/IPAM 必須完整符合 `rancher-cni-network` / `rancher-bridge` / `rancher-cni-ipam`；現行 `10-pasturestack.conf` 則必須完整符合 `pasturestack-cni-network` / `pasture-bridge` / `metadata-cni-ipam`。選定的 provider 再次需要歷史設定時，也會套用相同的身分判定。

退役時會將舊檔更名為加上 `.pasturestack-retired` 後綴的備份，保留原始位元組，並移出 CNI `.conf` / `.json` 執行集合。若備份已存在，其內容必須完全一致；內容衝突則明確報錯。管理者的其他設定會保留；格式損壞、只符合部分平台身分、符號連結及不安全的中繼資料路徑都會明確報錯。此次遷移不會掃除整個設定目錄，也不會移除 CNI 執行檔別名。

官方 `v0.8.22` Release 在 `2026-10-07T02:47:02Z` 下載弱點資料庫後，以 Trivy `0.74.0` 通過全嚴重程度的執行環境弱點與機密資料掃描。發布映像與 SBOM 均指向來源 commit `7b0920aa0c8f3b2c009c9c47c94c4d21b77c7077`。此版本仍須以正式映像完成受管升級驗收；元件發布並不代表既有基礎架構堆疊已完成升級。

## Provider 與生命週期收斂

管理器會依本機主機上的基礎架構服務中繼資料，為每個 CNI 執行檔選出唯一合格的 provider。數字型 OCI 映像版本以最高版為準；未標示版本或非數字的開發標籤不得取代正式數字版本，版本相同時再以不可變的容器 ID 做固定排序。產生的 wrapper 只綁定這個精確 provider，呼叫時不會再以服務標籤重新列舉容器。它優先執行 provider 私有的 `/opt/cni/bin` 程式，並只為舊映像保留有限的相容路徑。wrapper 以排他暫存 inode 與原子更名更新；內容、檔案型態或權限漂移時會安全修復，不會沿著遭置換的符號連結寫入。

若平台中繼資料暫時先出現主機連接埠容器、尚未填入主要位址，管理器可讀取該精確執行中容器的網路命名空間。只有該網路設定之受管子網路內恰好一個 IPv4 位址可被接受，讀取後還會再次確認同一 Docker 容器 PID。缺少、歧義、超出子網路或生命週期競態都會安全失敗，並保留上一份可用的主機連接埠規則，直到中繼資料與 CNI 完成收斂。

## 防火牆後端

`FIREWALL_BACKEND` 預設為 `auto`，依 Docker 實際防火牆驅動程式選擇單一路徑：Docker 原生 `nftables` 使用原生 nft 規則；Docker `iptables` 驅動程式則辨識哪一套前端擁有 Docker 現役 NAT 鏈。任何受支援主機（包括 Ubuntu 26.04 及更新版）都可能使用 `iptables-nft` 或 `iptables-legacy`；作業系統版本、執行檔存在或尚未載入的核心模組，均不足以決定後端。需要固定路徑時可選：

- `nftables`：Docker 原生 nftables 防火牆後端，**不是** iptables-nft 相容命令。
- `iptables-nft`：由 nf_tables 支援的 xtables 相容命令，搭配 Docker 的 iptables 防火牆驅動程式。
- `iptables-legacy`：只在現役 Docker 確實透過這套前端持有規則時選用。

選擇與 Docker 實際後端不符或無法判定時，管理器會拒絕啟動，不會自動降級、切換 Docker 後端或載入 legacy 模組。Ubuntu 26.04 及更新版若已使用 `iptables-legacy` 或 `iptables-nft`，就應維持現役 Docker 路徑；不能只因系統較新便替它切成原生 nftables。刻意遷移須另外準備主機變更、回復點及網路生命週期驗收。

主機 NAT 與主機連接埠的 `CATTLE_*` 規則鏈只由此管理器維護；三種後端的來源位址轉換規則都排除受管 overlay 子網路內的目的位址。每主機子網路還會排除其他有效主機的已驗證子網路，並加入限定來源與目的子網路的轉送例外；非現役主機不列入，現役主機若缺少標籤或子網路重疊則安全地拒絕套用。此網路只提供路由、不加密，須另行保護主機間傳輸。IPsec 主機 XFRM 路由器不得再插入補丁規則。升級時應先升級網路服務，逐台確認管理器健康，再升級相符的 IPsec 加密網路版本。

只有 CNI 中繼資料明確設定 `allowSharedSubnetIngress: true` 時才啟用共用子網路輸入轉送；為維持既有固定子網路契約相容性，同時具有 `bridgeSubnet` 與 `hostNat: true` 的舊設定也會採用相同行為。使用主機標籤決定子網路時會拒絕此選項，只信任已驗證的現役對端範圍。

使用 Docker 原生 nftables 前，必須先在主機 Docker 設定加入 `"firewall-backend": "nftables"` 及 `"bridge-accept-fwmark": "0x1068/0x1068"`，再升級此堆疊。還須在主機持久設定 `net.ipv4.ip_forward=1`，並於重開機後確認仍啟用；Docker 原生 nftables 後端不會代為啟用 IPv4 轉送。此標記讓 Docker 網橋轉送規則接受管理器發布的主機連接埠流量；範本無法替主機設定 Docker daemon 或核心參數。切換前還須檢查並明確遷移殘留的 `iptables-nft FORWARD DROP` 全域政策與舊平台掛鉤。管理器遇到混用狀態會拒絕啟動，不會自行修改主機全域防火牆政策。Docker 原生 nftables 目前仍屬實驗性功能，正式環境使用前應針對安裝的 Docker 版本完成驗收。

## 其他設定

- `DOCKER_BRIDGE`：受管工作負載使用的主機網橋。
- `DNS_RECURSER_TIMEOUT`、`TTL`：上游 DNS 逾時與服務探索快取時間。
- `CPU_PERIOD`、`CPU_QUOTA`：中繼資料服務的 CPU 排程限制。
- `RELOAD_INTERVAL_LIMIT`、`ARP_SYNC_INTERVAL`：中繼資料重新載入與主機 ARP 協調間隔。

網路外掛管理器仍需主機網路、主機 PID、Docker Socket、Docker 狀態、核心模組與執行環境掛載，以及共用 CNI 磁碟區。中繼資料服務僅在指派連結本機位址時以 root 啟動，之後切換為 UID/GID 10001；內部 DNS 與其共用網路命名空間。`rancher-compose.yml`、`io.rancher.*`、`CATTLE_*` 備援變數、`/var/lib/rancher` CA 路徑及 `rancher-cni-driver` 磁碟區是既有協定的相容契約，不代表必須使用 legacy 防火牆規則。

範本檔案採 MIT 授權；管理器、中繼資料服務與內部 DNS 保留 Apache-2.0 授權及隨附相依套件聲明。部署前應以 `catalog-images.json` 核對映像來源與記錄的 manifest digest。
