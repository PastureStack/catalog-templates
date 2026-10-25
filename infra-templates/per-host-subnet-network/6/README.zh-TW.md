<!-- SPDX-License-Identifier: MIT -->

# PastureStack 每台主機獨立子網路 v0.3.4 候選版

## 目前來源候選

本來源只準備數字修訂 6，尚未發布或部署。目前已發布的安裝座標仍是 Catalog v0.3.16 與數字修訂 5。新元件的 digest、producer、SBOM 與掃描收據尚待提供，因此不宣稱新成品已通過驗收；目前仍會被 image 發布證據 gate 阻擋。

預計替換的映像（已發布輸入 → 尚未發布候選）：

- `ghcr.io/pasturestack/ipsec-vxlan-overlay-network:v0.14.40` → `ghcr.io/pasturestack/ipsec-vxlan-overlay-network:v0.14.41`

除了這些映像 tag 與 Catalog 顯示版號，runtime 定義逐位元組保留原修訂。命令、預設值、資源參數、權限、附屬容器、磁碟區、防火牆選項與 plugin 職責都沿用既有契約。取得真實發布證據後才能提升本來源候選。

## 已發布修訂 5 的參考說明

以下相容性說明與驗證陳述只對應先前已發布的輸入，不能作為新候選映像的驗收證據。

此基礎架構範本會為每台主機分配不同的工作負載子網路，並維護這些
子網路之間帶有專用標記的主機閘道路由。部署前，請為每台參與主機
新增唯一標籤：

```text
io.pasturestack.network.per-host-subnet.subnet=10.50.1.0/24
```

每台主機必須使用互不重疊的子網路。可用
`io.pasturestack.network.per-host-subnet.range-start` 與
`io.pasturestack.network.per-host-subnet.range-end` 限制分配範圍。
只有中繼資料沒有提供其他主機可路由的位址時，控制器才會接受
`io.pasturestack.network.per-host-subnet.override-agent-ip`。

此範本使用
`ghcr.io/pasturestack/ipsec-vxlan-overlay-network:v0.14.40`。
映像原始碼位於
[`PastureStack/ipsec-vxlan-overlay-network@4711833178a05e5d225e364cce856bd108bdc707`](https://github.com/PastureStack/ipsec-vxlan-overlay-network/tree/4711833178a05e5d225e364cce856bd108bdc707)，
隨附控制器來自
[`PastureStack/per-host-subnet@v0.2.5`](https://github.com/PastureStack/per-host-subnet/releases/tag/v0.2.5)，
隨附 IPAM 執行檔來自
[`PastureStack/host-local-cni-ipam@v0.1.6`](https://github.com/PastureStack/host-local-cni-ipam/releases/tag/v0.1.6)。

範本檔案與圖示採 MIT 授權；執行專案採 Apache-2.0 授權。作業系統
套件及隨附元件保留各自的上游授權及聲明。

第 4 版會把 Catalog 的布林除錯選項明確保留為 CNI JSON 所要求的字串，
避免受管工作負載建立時發生型別解析錯誤。第 3 版透過控制平面實際提供的
純文字 `/self/host/labels/<key>`
端點解析主機專屬網橋及 IPAM 標籤；舊版將回應誤當 JSON，會使真機
受管工作負載建立失敗。子網路標籤必須有效且互不重疊，網路外掛管理器
會在套用主機防火牆規則前驗證。本驅動程式為選用功能，不會另外建立
商店供應者，也不會自動取代加密的 IPsec 覆疊網路。
