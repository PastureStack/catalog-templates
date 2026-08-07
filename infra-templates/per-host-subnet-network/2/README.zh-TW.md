# PastureStack 每台主機獨立子網路

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
`ghcr.io/pasturestack/ipsec-vxlan-overlay-network:v0.14.26`。
映像原始碼位於
[`PastureStack/ipsec-vxlan-overlay-network@e80db2268c9c0182b3b627e0c185998d9db91524`](https://github.com/PastureStack/ipsec-vxlan-overlay-network/tree/e80db2268c9c0182b3b627e0c185998d9db91524)，
隨附控制器來自
[`PastureStack/per-host-subnet@babe7d7f2b7f67a18883b9ed99d17483c8854315`](https://github.com/PastureStack/per-host-subnet/tree/babe7d7f2b7f67a18883b9ed99d17483c8854315)，
隨附 IPAM 執行檔來自
[`PastureStack/host-local-cni-ipam@e79e1721f78a9579145cd89d8ad5083ae24633f5`](https://github.com/PastureStack/host-local-cni-ipam/tree/e79e1721f78a9579145cd89d8ad5083ae24633f5)。

範本檔案與圖示採 MIT 授權；執行專案採 Apache-2.0 授權。作業系統
套件及隨附元件保留各自的上游授權及聲明。
