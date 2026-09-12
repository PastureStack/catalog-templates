<!-- SPDX-License-Identifier: MIT -->

# PastureStack 網路服務

此版本為網路外掛管理器新增單一、可選擇的主機防火牆後端；中繼資料服務與內部 DNS 沿用版本 3。候選範本指向已正式發布的網路外掛管理器 `v0.8.12`，來源 revision 與映像 manifest digest 已記錄於 `catalog-images.json`。這份商店候選仍須完成各後端的主機生命週期驗收，才可部署。

## 防火牆後端

`FIREWALL_BACKEND` 預設為 `auto`，依 Docker 實際防火牆驅動程式選擇單一路徑：Docker 原生 `nftables` 使用原生 nft 規則；Docker `iptables` 驅動程式則辨識哪一套前端擁有 Docker 現役 NAT 鏈。在舊主機上若 Docker 實際使用 legacy，也會選用該前端；僅有 legacy 執行檔並不足以啟用它。需要固定路徑時可選：

- `nftables`：Docker 原生 nftables 防火牆後端，**不是** iptables-nft 相容命令。
- `iptables-nft`：由 nf_tables 支援的 xtables 相容命令，搭配 Docker 的 iptables 防火牆驅動程式。
- `iptables-legacy`：只供明確使用舊版 xtables 的舊主機選用。

選擇與 Docker 實際後端不符時，管理器會拒絕啟動，不會自動降級或載入 legacy 模組。Ubuntu 26.04 的 nft-only 主機不應選擇 `iptables-legacy`。

使用 Docker 原生 nftables 前，必須先在主機 Docker 設定加入 `"firewall-backend": "nftables"` 及 `"bridge-accept-fwmark": "0x1068/0x1068"`，再升級此堆疊。還須在主機持久設定 `net.ipv4.ip_forward=1`，並於重開機後確認仍啟用；Docker 原生 nftables 後端不會代為啟用 IPv4 轉送。此標記讓 Docker 網橋轉送規則接受管理器發布的主機連接埠流量；範本無法替主機設定 Docker daemon 或核心參數。切換前還須檢查並明確遷移殘留的 `iptables-nft FORWARD DROP` 全域政策與舊平台掛鉤。管理器遇到混用狀態會拒絕啟動，不會自行修改主機全域防火牆政策。Docker 原生 nftables 目前仍屬實驗性功能，正式環境使用前應針對安裝的 Docker 版本完成驗收。

## 其他設定

- `DOCKER_BRIDGE`：受管工作負載使用的主機網橋。
- `DNS_RECURSER_TIMEOUT`、`TTL`：上游 DNS 逾時與服務探索快取時間。
- `CPU_PERIOD`、`CPU_QUOTA`：中繼資料服務的 CPU 排程限制。
- `RELOAD_INTERVAL_LIMIT`、`ARP_SYNC_INTERVAL`：中繼資料重新載入與主機 ARP 協調間隔。

網路外掛管理器仍需主機網路、主機 PID、Docker Socket、Docker 狀態、核心模組與執行環境掛載，以及共用 CNI 磁碟區。中繼資料服務僅在指派連結本機位址時以 root 啟動，之後切換為 UID/GID 10001；內部 DNS 與其共用網路命名空間。`rancher-compose.yml`、`io.rancher.*`、`CATTLE_*` 備援變數、`/var/lib/rancher` CA 路徑及 `rancher-cni-driver` 磁碟區是既有協定的相容契約，不代表必須使用 legacy 防火牆規則。

範本檔案採 MIT 授權；管理器、中繼資料服務與內部 DNS 保留 Apache-2.0 授權及隨附相依套件聲明。部署前應以 `catalog-images.json` 核對映像來源與記錄的 manifest digest。
