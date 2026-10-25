<!-- SPDX-License-Identifier: MIT -->

# PastureStack Windows 容器網路 v0.1.2 候選版

## 目前來源候選

本來源只準備數字修訂 4，尚未發布或部署。目前已發布的安裝座標仍是 Catalog v0.3.16 與數字修訂 3。新元件的 digest、producer、SBOM 與掃描收據尚待提供，因此不宣稱新成品已通過驗收；目前仍會被 image 發布證據 gate 阻擋。

預計替換的映像（已發布輸入 → 尚未發布候選）：

- `ghcr.io/pasturestack/pod-pause-image:v3.0.5` → `ghcr.io/pasturestack/pod-pause-image:v3.0.6`

除了這些映像 tag 與 Catalog 顯示版號，runtime 定義逐位元組保留原修訂。命令、預設值、資源參數、權限、附屬容器、磁碟區、防火牆選項與 plugin 職責都沿用既有契約。取得真實發布證據後才能提升本來源候選。

## 已發布修訂 3 的參考說明

以下相容性說明與驗證陳述只對應先前已發布的輸入，不能作為新候選映像的驗收證據。

此基礎架構項目會定義相容 Windows 容器工作負載使用的 `nat` 與 `transparent`
Docker 網路驅動程式。請在 PastureStack Windows 網路服務之前安裝。

PastureStack 是獨立的社群計畫，目的在保存、稽核與現代化 Rancher 1.6
生態系；本計畫與 Rancher Labs 或 SUSE 無隸屬或背書關係。

Compose 服務只用來選取既有 Windows 代理程式；相容服務結構雖然要求提供映像，
但不會將該映像當成 Windows 工作負載啟動。歷史選取值僅屬控制協定識別值，
不能在尚未同步更換 Windows 代理程式契約前單獨移除。

此範本已通過 Catalog Service 解析，並限制於 Windows 協調模式。由於目前沒有
Windows 主機完成網路驅動程式的端對端驗證，此項目仍屬候選版本。
