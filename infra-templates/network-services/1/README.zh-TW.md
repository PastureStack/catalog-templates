<!-- SPDX-License-Identifier: MIT -->

# PastureStack 網路服務

此基礎架構堆疊會在每台符合條件的主機上安裝網路外掛管理器、中繼
資料服務及內部 DNS。三者共同提供受管工作負載所需的主機 CNI 設定、
網路驅動程式包裝、工作負載中繼資料、服務探索、主機路由、主機連接埠
規則及網路協調。

三個映像都由 PastureStack 公開於 GHCR，並以語意化版本標籤引用。
已發布的版本標籤不會覆寫，發布總和檢查碼另行保存驗證證據。此堆疊
已與中繼資料健康檢查及 IPsec 加密網路共同通過單一主機整合測試。
請先安裝並啟用中繼資料健康檢查，再安裝此堆疊，最後才安裝 IPsec
加密網路。完整多主機受管網路生命週期通過前，此堆疊仍屬候選版本。

## 設定

- `DOCKER_BRIDGE`：受管工作負載流量使用的主機網橋。
- `DNS_RECURSER_TIMEOUT`：上游 DNS 查詢逾時。
- `TTL`：內部服務探索快取時間。
- `CPU_PERIOD` 與 `CPU_QUOTA`：限制中繼資料服務的 CPU 使用量。
- `RELOAD_INTERVAL_LIMIT`：限制中繼資料設定重新載入頻率。
- `ARP_SYNC_INTERVAL`：主機 ARP 協調間隔。

## 權限界線

網路外掛管理器會使用主機網路、主機 PID、Docker Socket、Docker
狀態、核心模組、執行環境掛載及共用 CNI 磁碟區。中繼資料服務會從
相容控制平面取得範圍受限的執行個體登入資訊，並管理連結本機中繼資料
位址。映像入口程式只會以 root 指派該位址，隨後切換成 UID/GID
`10001` 再啟動服務。內部 DNS 與中繼資料服務共用網路命名空間。

`rancher-compose.yml`、`io.rancher.*` 標籤、`CATTLE_*` 備援
變數、`/var/lib/rancher` CA 路徑及 `rancher-cni-driver` 磁碟區
是既有控制協定使用的相容契約，不是目前的產品品牌。未同步更新產生端
與使用端前，不可單獨移除。

## 授權與出處

範本檔案是 PastureStack 依 MIT 授權提供的新貢獻。網路外掛管理器、
中繼資料服務及內部 DNS 均採 Apache-2.0 授權；Ubuntu 與隨附相依
套件保留各自的授權及聲明。審核過的原始碼修訂與映像界線請參閱原始碼
儲存庫及 `catalog-images.json`。
