<!-- SPDX-License-Identifier: MIT -->

# 中繼資料健康檢查

修訂 5 使用已發行的 `ghcr.io/pasturestack/metadata-healthcheck:v0.3.20`，
包含 Ubuntu HAProxy 3.2.25-0ubuntu0.26.04.2 及 Perl、CA、APT 官方更新。
回復時可使用修訂 4 的 `ghcr.io/pasturestack/metadata-healthcheck:v0.3.19`。

代理從連結本機的 Metadata 端點讀取健康檢查設定，
並使用權限受限的代理憑證回報狀態。TCP 42 仍為容器就緒端點。

可在[映像發行頁](https://github.com/PastureStack/metadata-healthcheck/releases/tag/v0.3.20)
及 `catalog-images.json` 查閱映像識別、SBOM 與掃描證據。
