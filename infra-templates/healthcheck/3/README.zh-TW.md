<!-- SPDX-License-Identifier: MIT -->

# 中繼資料健康檢查 v0.3.18 候選版

## 目前來源候選

本來源只準備數字修訂 3，尚未發布或部署。目前已發布的安裝座標仍是 Catalog v0.3.16 與數字修訂 2。新元件的 digest、producer、SBOM 與掃描收據尚待提供，因此不宣稱新成品已通過驗收；目前仍會被 image 發布證據 gate 阻擋。

預計替換的映像（已發布輸入 → 尚未發布候選）：

- `ghcr.io/pasturestack/metadata-healthcheck:v0.3.17` → `ghcr.io/pasturestack/metadata-healthcheck:v0.3.18`

除了這些映像 tag 與 Catalog 顯示版號，runtime 定義逐位元組保留原修訂。命令、預設值、資源參數、權限、附屬容器、磁碟區、防火牆選項與 plugin 職責都沿用既有契約。取得真實發布證據後才能提升本來源候選。

## 已發布修訂 2 的參考說明

以下相容性說明與驗證陳述只對應先前已發布的輸入，不能作為新候選映像的驗收證據。

此基礎架構堆疊會在每台符合條件的主機上執行一個健康檢查代理程式。
代理程式從既有的連結本機中繼資料端點讀取健康狀態宣告、管理自己的
HAProxy 處理程序，並把穩定的狀態變更回報給相容控制 API。

### 已審核映像

- 映像：`ghcr.io/pasturestack/metadata-healthcheck:v0.3.17`
- 原始碼：
  [`PastureStack/metadata-healthcheck@410993d3b3b2493bbd84a36f7d67cfefb8dd6705`](https://github.com/PastureStack/metadata-healthcheck/tree/410993d3b3b2493bbd84a36f7d67cfefb8dd6705)
- 原始碼採 Apache-2.0 授權；作業系統套件保留各自的上游授權。
- Trivy 結果為 HIGH 0、CRITICAL 0，映像及原始碼的機密資料掃描均為 0。
- 公開 GHCR 與未登入拉取版本標籤的驗證已通過。

### 相容性界線

相容控制平面仍需要名為 `rancher-compose.yml` 的檔案及
`io.rancher.*` 標籤。這些是協定識別名稱，不是目前的產品品牌。
`create_agent` 流程會提供範圍受限的執行個體登入資訊；若未明確設定
中性名稱，映像才會把相容名稱轉換成公開的 `PLATFORM_*` 設定。

`PLATFORM_CA_ROOT` 指向既有的唯讀代理程式憑證掛載。容器網路上的
TCP 42 是就緒狀態端點，不會公開成主機連接埠。此範本不會掛載 Docker
Socket、不要求特權模式，也不新增 Linux Capability。

### 發布界線

映像層級的整合測試已使用預設連結本機位址通過，且不依賴中性的
中繼資料 DNS 別名；一般生命週期訊息會寫入標準輸出，只有實際失敗
才會寫入標準錯誤。較早的商店部署也驗證過登入資訊注入、相容名稱
映射、全域排程、就緒狀態、重新啟動、雙常駐程式回報及移除流程。
多主機升級、回復及完整基礎架構堆疊移除仍須在隔離 VM 快照完成
部署驗收。請勿使用此範本直接變更既有的
正式控制平面。
