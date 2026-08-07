<!-- SPDX-License-Identifier: MIT -->

# 中繼資料健康檢查 v0.3.15

此基礎架構堆疊會在每台符合條件的主機上執行一個健康檢查代理程式。
代理程式從既有的連結本機中繼資料端點讀取健康狀態宣告、管理自己的
HAProxy 處理程序，並把穩定的狀態變更回報給相容控制 API。

## 已審核映像

- 映像：`ghcr.io/pasturestack/metadata-healthcheck:v0.3.15`
- 原始碼：
  [`PastureStack/metadata-healthcheck@b7ca40062ae22988c0c40af05eafe5b1ee8846bc`](https://github.com/PastureStack/metadata-healthcheck/tree/b7ca40062ae22988c0c40af05eafe5b1ee8846bc)
- 原始碼採 Apache-2.0 授權；作業系統套件保留各自的上游授權。
- Trivy 結果為 HIGH 0、CRITICAL 0，映像及原始碼的機密資料掃描均為 0。
- 公開 GHCR 與未登入拉取版本標籤的驗證已通過。

## 相容性界線

相容控制平面仍需要名為 `rancher-compose.yml` 的檔案及
`io.rancher.*` 標籤。這些是協定識別名稱，不是目前的產品品牌。
`create_agent` 流程會提供範圍受限的執行個體登入資訊；若未明確設定
中性名稱，映像才會把相容名稱轉換成公開的 `PLATFORM_*` 設定。

`PLATFORM_CA_ROOT` 指向既有的唯讀代理程式憑證掛載。容器網路上的
TCP 42 是就緒狀態端點，不會公開成主機連接埠。此範本不會掛載 Docker
Socket、不要求特權模式，也不新增 Linux Capability。

## 發布界線

映像層級的整合測試已使用預設連結本機位址通過，且不依賴中性的
中繼資料 DNS 別名。較早的商店部署也驗證過登入資訊注入、相容名稱
映射、全域排程、就緒狀態、重新啟動、雙常駐程式回報及移除流程。
在 v0.3.15 於隔離 VM 快照完成新的多主機升級、回復及完整基礎架構
堆疊移除測試前，此範本仍屬候選版本。請勿使用此範本直接變更既有的
正式控制平面。
