<!-- SPDX-License-Identifier: MIT -->

# 中繼資料健康檢查

數字修訂 4 使用已發布的 `ghcr.io/pasturestack/metadata-healthcheck:v0.3.19`。
舊修訂 3 與 `ghcr.io/pasturestack/metadata-healthcheck:v0.3.18` 保留可用。
問題、服務設定、排程與權限均沿用既有契約。

此基礎架構堆疊會在每台符合條件的主機執行健康檢查代理程式。
代理程式從既有連結本機中繼資料端點讀取健康狀態宣告，管理自己的
HAProxy 處理程序，並把穩定的狀態變更回報給相容控制 API。

## 映像與相容性

- 映像：`ghcr.io/pasturestack/metadata-healthcheck:v0.3.19`
- 原始碼：[PastureStack/metadata-healthcheck@6fd1fa81623dc9061d6b72a7a4d4b1c5d3b5fc37](https://github.com/PastureStack/metadata-healthcheck/tree/6fd1fa81623dc9061d6b72a7a4d4b1c5d3b5fc37)
- 原始碼採 Apache-2.0 授權；隨附套件保留各自的上游授權與聲明。
- 精準 manifest digest、runtime SBOM、原始／有效發現及發布證據記錄於 `catalog-images.json`。

相容控制平面仍需要 `rancher-compose.yml` 檔名及 `io.rancher.*` 協定標籤。
`create_agent` 提供範圍受限的執行個體登入資訊；只有未明確設定中性名稱時，
才會把相容名稱映射到公開的 `PLATFORM_*` 設定。

`PLATFORM_CA_ROOT` 使用既有唯讀代理程式憑證掛載。容器網路 TCP 42 是就緒
端點，不會公開成主機連接埠。範本不掛載 Docker socket、不要求特權模式，
也不新增 Linux capability。

## 升級界線

已發布映像的驗證與官方未修補 Low/Medium 追蹤，均和部署驗收分開。
保留既有生命週期證據，變更既有安裝前再確認受影響的 readiness 路徑及
主機受管升級／回復。映像發布不代表重新通過完整角色或主機矩陣。
