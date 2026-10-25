<!-- SPDX-License-Identifier: MIT -->

# 系統映像預先下載

此全域且啟動一次的服務會讀取系統堆疊映像參照，並請各主機 Docker daemon 快取尚未存在的映像。

數字修訂 5（顯示版本 `v0.3.4`）使用已發布的 `ghcr.io/pasturestack/system-image-preloader:v0.3.4`。
舊修訂 4 及 `ghcr.io/pasturestack/system-image-preloader:v0.3.3` 保留可用。
問題、環境、資源參數、磁碟區、權限與 plugin 職責不變。
精準發布記錄見 `catalog-images.json`，環境驗收仍須分開確認。

### 已審核映像

- 映像：`ghcr.io/pasturestack/system-image-preloader:v0.3.4`
- 原始碼：
  [`PastureStack/system-image-preloader@624a45cd001a92cdf5132f487ba14e161dff40d2`](https://github.com/PastureStack/system-image-preloader/tree/624a45cd001a92cdf5132f487ba14e161dff40d2)
- 原始碼採 Apache-2.0 授權；Ubuntu、Docker CLI、`yq`、`gomplate`
  及相依套件保留各自的上游授權及聲明。
- 完整嚴重度掃描沒有可用修補、未審核項目或機密資料；官方尚無修補的 Low/Medium 持續追蹤。
- 公開 GHCR 與未登入存取版本標籤的驗證已通過。

### 安全性界線

此服務需要以讀寫方式掛載 `/var/run/docker.sock`。Docker Socket
權限等同主機管理者權限，因此只能部署經審核的映像，並限制可編輯此
堆疊的使用者。服務會自動取得範圍受限的相容 API 登入資訊，且不會
啟用可能顯示登入資訊的 Shell 追蹤。

私有登錄登入資訊為選用功能。啟用後，選取的主機 Docker
`config.json` 會以唯讀方式掛載。特權模式預設關閉，只能在主機
安全性政策確實要求時啟用。映像拉取重試與 CPU 使用量等待都有明確
上限。

相容控制平面仍需要名為 `rancher-compose.yml` 的檔案及
`io.rancher.*` 代理程式與排程標籤。這些是協定識別名稱，不是目前
的產品品牌。

### 驗證

已發布映像身分、執行期 SBOM、原始與有效發現，以及套件安裝驗證均記錄於
`catalog-images.json`。Catalog 來源與 API 契約驗證新版預設值及保留修訂。
受管主機上的映像快取、升級與回復驗收，仍須依實際環境另外確認。
