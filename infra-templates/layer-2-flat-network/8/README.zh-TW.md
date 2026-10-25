<!-- SPDX-License-Identifier: MIT -->

# PastureStack 第 2 層平面網路 v0.3.6 候選版

## 目前來源候選

本來源只準備數字修訂 8，尚未發布或部署。目前已發布的安裝座標仍是 Catalog v0.3.16 與數字修訂 7。新元件的 digest、producer、SBOM 與掃描收據尚待提供，因此不宣稱新成品已通過驗收；目前仍會被 image 發布證據 gate 阻擋。

預計替換的映像（已發布輸入 → 尚未發布候選）：

- `ghcr.io/pasturestack/ipsec-vxlan-overlay-network:v0.14.40` → `ghcr.io/pasturestack/ipsec-vxlan-overlay-network:v0.14.41`

除了這些映像 tag 與 Catalog 顯示版號，runtime 定義逐位元組保留原修訂。命令、預設值、資源參數、權限、附屬容器、磁碟區、防火牆選項與 plugin 職責都沿用既有契約。取得真實發布證據後才能提升本來源候選。

## 已發布修訂 7 的參考說明

以下相容性說明與驗證陳述只對應先前已發布的輸入，不能作為新候選映像的驗收證據。

此基礎架構範本會透過主機網橋，將受管工作負載直接連接到共用的實體
第 2 層子網路。每台參與主機都必須能連上相同的子網路與閘道，而且
選定的工作負載位址範圍不得與 DHCP、主機或基礎架構位址重疊。

自動設定網橋預設為停用。若實體介面、子網路或閘道設定錯誤，把主機
實體介面移入網橋可能會中斷遠端連線。請優先透過作業系統準備網橋；
若要啟用自動設定，請先確認具備頻外主控台存取方式。

此範本使用
`ghcr.io/pasturestack/ipsec-vxlan-overlay-network:v0.14.40`，
其中包含經審核的 `pasture-bridge` 與 `flat-cni-ipam` 執行檔。
映像原始碼位於
[`PastureStack/ipsec-vxlan-overlay-network@4711833178a05e5d225e364cce856bd108bdc707`](https://github.com/PastureStack/ipsec-vxlan-overlay-network/tree/4711833178a05e5d225e364cce856bd108bdc707)，
Flat CNI IPAM 原始碼位於
[`PastureStack/flat-cni-ipam@v0.1.6`](https://github.com/PastureStack/flat-cni-ipam/releases/tag/v0.1.6)。

範本檔案與圖示採 MIT 授權；執行專案採 Apache-2.0 授權。作業系統
套件及隨附元件保留各自的上游授權及聲明。

第 6 版保留第 5 版的除錯選項型別與網橋權責。Flat IPAM 現在會區分
明確的主機位址與網路前綴：明確位址會原樣保留；若設定的是網路前綴，
只有當第一個可用位址確實存在於網橋時才會選用。多位址網橋若仍有歧義，
會停止配置而不擅自猜測。此變更不改動防火牆、IPsec、VXLAN 或實體介面
設定。啟用此選用驅動程式前，仍須驗證真實第 2 層連線及回復方式。
