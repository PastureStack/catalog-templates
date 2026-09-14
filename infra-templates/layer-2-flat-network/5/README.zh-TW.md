# PastureStack 第 2 層平面網路

此基礎架構範本會透過主機網橋，將受管工作負載直接連接到共用的實體
第 2 層子網路。每台參與主機都必須能連上相同的子網路與閘道，而且
選定的工作負載位址範圍不得與 DHCP、主機或基礎架構位址重疊。

自動設定網橋預設為停用。若實體介面、子網路或閘道設定錯誤，把主機
實體介面移入網橋可能會中斷遠端連線。請優先透過作業系統準備網橋；
若要啟用自動設定，請先確認具備頻外主控台存取方式。

此範本使用
`ghcr.io/pasturestack/ipsec-vxlan-overlay-network:v0.14.36`，
其中包含經審核的 `pasture-bridge` 與 `flat-cni-ipam` 執行檔。
映像原始碼位於
[`PastureStack/ipsec-vxlan-overlay-network@f754bab6dc63c4e51b849a106fcdc792f644b9ef`](https://github.com/PastureStack/ipsec-vxlan-overlay-network/tree/f754bab6dc63c4e51b849a106fcdc792f644b9ef)，
Flat CNI IPAM 原始碼位於
[`PastureStack/flat-cni-ipam@047eb2ffc5a985810fbc8a9a25150698facc6ae6`](https://github.com/PastureStack/flat-cni-ipam/tree/047eb2ffc5a985810fbc8a9a25150698facc6ae6)。

範本檔案與圖示採 MIT 授權；執行專案採 Apache-2.0 授權。作業系統
套件及隨附元件保留各自的上游授權及聲明。

第 5 版會把 Catalog 的布林除錯選項明確保留為 CNI JSON 所要求的字串，
避免受管工作負載建立時發生型別解析錯誤。此版隨附會遵守
`skipBridgeConfigureIP` 的橋接 CNI，保留已設定的網橋位址；不改變主機
網橋權責，也不自動搬移實體網路
介面。啟用此選用驅動程式前，仍須驗證真實第 2 層連線及回復方式。
