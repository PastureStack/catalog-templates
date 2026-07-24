import json
import os
import subprocess
import sys
import tempfile
from urllib.request import urlopen

import pytest


def _base():
    return os.path.dirname(__file__)


def _file(f):
    return os.path.join(_base(), '../../{}'.format(f))


def _repo_root():
    return os.path.abspath(_file('./'))


class CatalogService(object):
    def __init__(self, catalog_bin):
        self.catalog_bin = catalog_bin

    def assert_retcode(self, ret_code, *args, **kw):
        p = self.call(*args, **kw)
        r_code = p.wait()
        assert r_code == ret_code

    def call(self, *args, **kw):
        cmd = [self.catalog_bin]
        cmd.extend(args)

        kw_args = {
            'stdin': subprocess.PIPE,
            'stdout': sys.stdout,
            'stderr': sys.stderr,
            'cwd': _base(),
        }

        kw_args.update(kw)
        return subprocess.Popen(cmd, **kw_args)


@pytest.fixture(scope='session')
def catalog_bin():
    c = os.environ.get('CATALOG_SERVICE_BIN')
    assert c
    assert os.path.isfile(c)
    assert os.access(c, os.X_OK)
    return c


@pytest.fixture(scope='session')
def catalog_service(catalog_bin):
    return CatalogService(catalog_bin)


def _current_branch():
    branch = os.environ.get('CATALOG_TEST_BRANCH')
    if branch:
        return branch
    return subprocess.check_output(
        ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
        cwd=_repo_root()).decode('utf-8').strip()


def _catalog_repo():
    return os.environ.get('CATALOG_TEST_REPO', _repo_root())


def _catalog_commit():
    commit = os.environ.get('CATALOG_TEST_COMMIT')
    if commit:
        return commit
    return subprocess.check_output(
        ['git', 'rev-parse', 'HEAD'],
        cwd=_repo_root()).decode('utf-8').strip()


def _catalog_config():
    data = {
        'catalogs': {
            'library': {
                'url': _catalog_repo(),
                'branch': _current_branch(),
                'pinnedCommit': _catalog_commit(),
            },
        },
    }
    f = tempfile.NamedTemporaryFile('w', delete=False)
    try:
        json.dump(data, f)
        return f.name
    finally:
        f.close()


def _get_json(url):
    with urlopen(url, timeout=10) as response:
        return json.loads(response.read().decode('utf-8'))


def test_validate_exits_normal(catalog_service):
    config = _catalog_config()
    with tempfile.TemporaryDirectory(
            prefix='pasturestack-catalog-validate-') as cache:
        catalog_service.assert_retcode(
            0,
            '--config', config,
            '--cache', cache,
            '--validate', '--sqlite', '--port', '18088',
            cwd=cache)
    os.remove(config)


def test_catalog_list():
    templates = _get_json('http://localhost:8088/v1-catalog/templates')
    data = templates.get('data', [])
    assert len(data) == 15
    by_folder = {
        (item.get('templateBase') or 'template', item['folderName']): item
        for item in data
    }
    assert set(by_folder) == {
        ('infra', 'amazon-ebs-storage'),
        ('infra', 'amazon-efs-storage'),
        ('infra', 'container-schedule'),
        ('infra', 'ecr-credential-sync'),
        ('infra', 'healthcheck'),
        ('infra', 'ipsec-overlay'),
        ('infra', 'layer-2-flat-network'),
        ('infra', 'network-services'),
        ('infra', 'nfs-storage'),
        ('infra', 'per-host-subnet-network'),
        ('infra', 'resource-scheduler'),
        ('infra', 'route53-dns-sync'),
        ('infra', 'system-image-preloader'),
        ('infra', 'vxlan-overlay-network'),
        ('project', 'native'),
    }
    assert by_folder[('infra', 'amazon-ebs-storage')][
        'name'] == 'PastureStack Amazon EBS Storage'
    assert by_folder[('infra', 'amazon-ebs-storage')][
        'defaultVersion'] == 'v0.10.0'
    assert by_folder[('infra', 'amazon-ebs-storage')][
        'links']['defaultVersion'].endswith(
        ':1')
    assert by_folder[('infra', 'amazon-efs-storage')][
        'name'] == 'PastureStack Amazon EFS Storage'
    assert by_folder[('infra', 'amazon-efs-storage')][
        'defaultVersion'] == 'v0.10.0'
    assert by_folder[('infra', 'amazon-efs-storage')][
        'links']['defaultVersion'].endswith(
        ':1')
    assert by_folder[('infra', 'container-schedule')][
        'name'] == 'PastureStack Container Schedule'
    assert by_folder[('infra', 'container-schedule')][
        'defaultVersion'] == 'v0.6.0'
    assert by_folder[('infra', 'container-schedule')][
        'links']['defaultVersion'].endswith(
        ':1')
    assert by_folder[('infra', 'ecr-credential-sync')][
        'name'] == 'PastureStack Amazon ECR Credential Sync'
    assert by_folder[('infra', 'ecr-credential-sync')][
        'defaultVersion'] == 'v3.1.0'
    assert by_folder[('infra', 'ecr-credential-sync')][
        'links']['defaultVersion'].endswith(
        ':1')
    assert by_folder[('infra', 'healthcheck')][
        'name'] == 'Metadata Healthcheck'
    assert by_folder[('infra', 'healthcheck')][
        'defaultVersion'] == 'v0.3.15'
    assert by_folder[('infra', 'ipsec-overlay')]['name'] == (
        'PastureStack IPsec Overlay')
    assert by_folder[('infra', 'ipsec-overlay')][
        'defaultVersion'] == '0.3.0-rc2'
    assert by_folder[('infra', 'ipsec-overlay')][
        'links']['defaultVersion'].endswith(
        ':1')
    assert by_folder[('infra', 'layer-2-flat-network')]['name'] == (
        'PastureStack Layer 2 Flat Network')
    assert by_folder[('infra', 'layer-2-flat-network')][
        'defaultVersion'] == '0.3.0-rc8'
    assert by_folder[('infra', 'layer-2-flat-network')][
        'links']['defaultVersion'].endswith(
        ':1')
    assert by_folder[('infra', 'network-services')]['name'] == (
        'PastureStack Network Services')
    assert by_folder[('infra', 'network-services')][
        'defaultVersion'] == '0.3.0-rc2'
    assert by_folder[('infra', 'network-services')][
        'links']['defaultVersion'].endswith(
        ':1')
    assert by_folder[('infra', 'nfs-storage')][
        'name'] == 'PastureStack NFS Storage'
    assert by_folder[('infra', 'nfs-storage')][
        'defaultVersion'] == 'v0.10.0'
    assert by_folder[('infra', 'nfs-storage')][
        'links']['defaultVersion'].endswith(
        ':1')
    assert by_folder[('infra', 'per-host-subnet-network')]['name'] == (
        'PastureStack Per-Host Subnet Network')
    assert by_folder[('infra', 'per-host-subnet-network')][
        'defaultVersion'] == '0.3.0-rc8'
    assert by_folder[('infra', 'per-host-subnet-network')][
        'links']['defaultVersion'].endswith(
        ':1')
    assert by_folder[('infra', 'resource-scheduler')][
        'name'] == 'Resource Scheduler'
    assert by_folder[('infra', 'resource-scheduler')][
        'defaultVersion'] == 'v0.8.15'
    assert by_folder[('infra', 'resource-scheduler')][
        'links']['defaultVersion'].endswith(
        ':1')
    assert by_folder[('infra', 'route53-dns-sync')][
        'name'] == 'PastureStack Route 53 DNS Sync'
    assert by_folder[('infra', 'route53-dns-sync')][
        'defaultVersion'] == 'v0.8.0'
    assert by_folder[('infra', 'route53-dns-sync')][
        'links']['defaultVersion'].endswith(
        ':1')
    assert by_folder[('infra', 'system-image-preloader')]['name'] == (
        'PastureStack System Image Preloader')
    assert by_folder[('infra', 'system-image-preloader')][
        'defaultVersion'] == 'v0.3.0'
    assert by_folder[('infra', 'system-image-preloader')][
        'links']['defaultVersion'].endswith(
        ':1')
    assert by_folder[('infra', 'vxlan-overlay-network')]['name'] == (
        'PastureStack VXLAN Overlay Network')
    assert by_folder[('infra', 'vxlan-overlay-network')][
        'defaultVersion'] == '0.3.0-rc9'
    assert by_folder[('infra', 'vxlan-overlay-network')][
        'links']['defaultVersion'].endswith(
        ':1')
    assert by_folder[('project', 'native')][
        'name'] == 'PastureStack Native'
    assert by_folder[('project', 'native')][
        'defaultVersion'] == '0.3.0-rc6'
    localized = {
        ('infra', 'amazon-ebs-storage'): (
            'PastureStack Amazon EBS 儲存空間',
            '掛載既有的 Amazon EBS 磁碟區；如需建立加密磁碟區，必須明確啟用雲端資源配置。'),
        ('infra', 'amazon-efs-storage'): (
            'PastureStack Amazon EFS 儲存空間',
            '掛載既有的 Amazon EFS 檔案系統；如需建立檔案系統與掛載目標，必須明確啟用雲端資源配置。'),
        ('infra', 'container-schedule'): (
            'PastureStack 容器定時排程',
            '依容器標籤中的 Cron 表達式，定時啟動、停止或重新啟動容器。'),
        ('infra', 'ecr-credential-sync'): (
            'PastureStack Amazon ECR 登入資訊同步',
            '定期更新 Amazon Elastic Container Registry 的短效登入資訊，並同步至目前或指定的環境。'),
        ('infra', 'healthcheck'): (
            '中繼資料健康檢查',
            '依據中繼資料定義檢查工作負載健康狀態，並透過相容控制 API 回報結果。'),
        ('infra', 'ipsec-overlay'): (
            'PastureStack IPsec 加密網路',
            '為受管工作負載提供跨主機的加密網路。'),
        ('infra', 'layer-2-flat-network'): (
            'PastureStack 第 2 層平面網路',
            '透過主機網橋，將受管理的工作負載直接連接到共用的第 2 層子網路。'),
        ('infra', 'network-services'): (
            'PastureStack 網路服務',
            '安裝受管工作負載所需的主機網路、中繼資料與內部 DNS 服務。'),
        ('infra', 'nfs-storage'): (
            'PastureStack NFS 儲存空間',
            '提供 NFS 第 3 版與第 4 版的 Docker 磁碟區，移除磁碟區時預設保留資料。'),
        ('infra', 'per-host-subnet-network'): (
            'PastureStack 每台主機獨立子網路',
            '為每台主機配置獨立的工作負載子網路，並維護主機間的閘道路由。'),
        ('infra', 'resource-scheduler'): (
            '資源排程器',
            '依控制平面事件與目前的中繼資料狀態，排程原生工作負載。'),
        ('infra', 'route53-dns-sync'): (
            'PastureStack Route 53 DNS 紀錄同步',
            '將相容環境的服務位址同步至指定的 Amazon Route 53 託管區域。'),
        ('infra', 'system-image-preloader'): (
            'PastureStack 系統映像預先下載',
            '預先下載相容基礎架構堆疊所需的容器映像，以縮短主機升級等待時間。'),
        ('infra', 'vxlan-overlay-network'): (
            'PastureStack VXLAN 覆疊網路',
            '透過 UDP 4789，在受管主機之間建立未加密的 VXLAN 覆疊網路。'),
        ('project', 'native'): (
            'PastureStack 原生專案範本',
            'PastureStack 原生編排執行環境的預設專案範本。'),
    }
    for key, (name, description) in localized.items():
        labels = by_folder[key]['labels']
        assert labels['io.pasturestack.catalog.name.zh-tw'] == name
        assert labels[
            'io.pasturestack.catalog.description.zh-tw'] == description


def test_catalog_compose_shapes_are_runtime_compatible():
    templates = _get_json('http://localhost:8088/v1-catalog/templates')
    by_folder = {
        (item.get('templateBase') or 'template', item['folderName']): item
        for item in templates.get('data', [])
    }

    ebs_version = _get_json(
        by_folder[('infra', 'amazon-ebs-storage')][
            'links']['defaultVersion'])
    ebs_files = ebs_version['files']
    ebs_docker = ebs_files['docker-compose.yml']
    ebs_platform = ebs_files['rancher-compose.yml']
    ebs_image = 'ghcr.io/pasturestack/ebs-storage-driver:v0.10.0'
    assert ebs_docker.count('image: {}'.format(ebs_image)) == 1
    assert '\n  amazon-ebs-storage-driver:\n' in ebs_docker
    assert 'privileged: true' in ebs_docker
    assert 'network_mode: host' in ebs_docker
    assert "ALLOW_CLOUD_PROVISIONING: '${ALLOW_CLOUD_PROVISIONING}'" in (
        ebs_docker)
    assert "AWS_ACCESS_KEY_ID: '${AWS_ACCESS_KEY_ID}'" in ebs_docker
    assert "AWS_SECRET_ACCESS_KEY: '${AWS_SECRET_ACCESS_KEY}'" in ebs_docker
    assert "AWS_SESSION_TOKEN: '${AWS_SESSION_TOKEN}'" in ebs_docker
    assert "AWS_REGION: '${AWS_REGION}'" in ebs_docker
    assert (
        '/var/lib/rancher/volumes:/var/lib/pasturestack/volumes:shared'
        in ebs_docker)
    assert '@sha256:' not in ebs_docker
    assert '\namazon-ebs-storage-driver:\n  storage_driver:' in ebs_platform
    assert 'name: pasturestack-ebs' in ebs_platform
    assert 'volume_access_mode: singleHostRW' in ebs_platform
    assert 'start_on_create: true' in ebs_platform
    assert 'default: false' in ebs_platform
    assert ebs_platform.count('type: password') == 2

    efs_version = _get_json(
        by_folder[('infra', 'amazon-efs-storage')][
            'links']['defaultVersion'])
    efs_files = efs_version['files']
    efs_docker = efs_files['docker-compose.yml']
    efs_platform = efs_files['rancher-compose.yml']
    efs_image = 'ghcr.io/pasturestack/efs-storage-driver:v0.10.0'
    assert efs_docker.count('image: {}'.format(efs_image)) == 1
    assert '\n  amazon-efs-storage-driver:\n' in efs_docker
    assert 'privileged: true' in efs_docker
    assert 'network_mode: host' in efs_docker
    assert "ALLOW_CLOUD_PROVISIONING: '${ALLOW_CLOUD_PROVISIONING}'" in (
        efs_docker)
    assert "AWS_ACCESS_KEY_ID: '${AWS_ACCESS_KEY_ID}'" in efs_docker
    assert "AWS_SECRET_ACCESS_KEY: '${AWS_SECRET_ACCESS_KEY}'" in efs_docker
    assert "AWS_SESSION_TOKEN: '${AWS_SESSION_TOKEN}'" in efs_docker
    assert "AWS_REGION: '${AWS_REGION}'" in efs_docker
    assert "EFS_SUBNET_ID: '${EFS_SUBNET_ID}'" in efs_docker
    assert "EFS_SECURITY_GROUP_ID: '${EFS_SECURITY_GROUP_ID}'" in efs_docker
    assert (
        '/var/lib/rancher/volumes:/var/lib/pasturestack/volumes:shared'
        in efs_docker)
    assert '0.0.0.0/0' not in efs_docker
    assert '@sha256:' not in efs_docker
    assert '\namazon-efs-storage-driver:\n  storage_driver:' in efs_platform
    assert 'name: pasturestack-efs' in efs_platform
    assert 'volume_access_mode: multiHostRW' in efs_platform
    assert 'start_on_create: true' in efs_platform
    assert 'default: false' in efs_platform
    assert efs_platform.count('type: password') == 2

    container_schedule_version = _get_json(
        by_folder[('infra', 'container-schedule')][
            'links']['defaultVersion'])
    container_schedule_files = container_schedule_version['files']
    container_schedule_docker = container_schedule_files[
        'docker-compose.yml.tpl']
    container_schedule_platform = container_schedule_files[
        'rancher-compose.yml']
    container_schedule_image = (
        'ghcr.io/pasturestack/container-cron:v0.6.0')
    assert container_schedule_docker.count(
        'image: {}'.format(container_schedule_image)) == 1
    assert '\n  container-schedule:\n' in container_schedule_docker
    assert '/var/run/docker.sock:/var/run/docker.sock' in (
        container_schedule_docker)
    assert "io.rancher.scheduler.global: 'true'" in (
        container_schedule_docker)
    assert 'container-cron' in container_schedule_docker
    assert 'ENABLE_DEBUG' in container_schedule_docker
    assert 'ENABLE_METRICS' in container_schedule_docker
    assert 'privileged: true' not in container_schedule_docker
    assert '@sha256:' not in container_schedule_docker
    assert 'minimum_rancher_version: v1.6.15-rc1' in (
        container_schedule_platform)

    ecr_version = _get_json(
        by_folder[('infra', 'ecr-credential-sync')][
            'links']['defaultVersion'])
    ecr_files = ecr_version['files']
    ecr_docker = ecr_files['docker-compose.yml.tpl']
    ecr_platform = ecr_files['rancher-compose.yml']
    ecr_image = 'ghcr.io/pasturestack/ecr-credential-sync:v3.1.0'
    assert ecr_docker.count('image: {}'.format(ecr_image)) == 1
    assert '\n  ecr-credential-sync:\n' in ecr_docker
    assert '$${PLATFORM_URL:-$${CATTLE_URL:-}}' in ecr_docker
    assert '$${PLATFORM_ACCESS_KEY:-$${CATTLE_ACCESS_KEY:-}}' in (
        ecr_docker)
    assert '$${PLATFORM_SECRET_KEY:-$${CATTLE_SECRET_KEY:-}}' in (
        ecr_docker)
    assert "io.rancher.container.agent.role: environment" in ecr_docker
    assert '/home/pasturestack/.aws:ro' in ecr_docker
    assert 'privileged: true' not in ecr_docker
    assert '/var/run/docker.sock' not in ecr_docker
    assert 'network_mode: host' not in ecr_docker
    assert '@sha256:' not in ecr_docker
    assert '{{- if' not in ecr_docker
    assert '{{- end' not in ecr_docker
    assert 'minimum_rancher_version: v1.6.13-rc1' in ecr_platform
    assert 'type: password' in ecr_platform
    assert 'request_line: GET /ping HTTP/1.0' in ecr_platform
    assert '\necr-credential-sync:\n  scale: 1' in ecr_platform

    health_version = _get_json(
        by_folder[('infra', 'healthcheck')]['links']['defaultVersion'])
    health_files = health_version['files']
    health_docker = health_files['docker-compose.yml']
    health_platform = health_files['rancher-compose.yml']
    health_image = 'ghcr.io/pasturestack/metadata-healthcheck:v0.3.15'
    assert "version: '2'\nservices:\n  healthcheck:" in health_docker
    assert health_docker.count('image: {}'.format(health_image)) == 1
    assert (
        '    - --metadata-url\n'
        '    - http://169.254.169.250/2015-12-19\n'
        in health_docker
    )
    assert 'http://metadata/' not in health_docker
    assert '\nservices:\n' not in health_platform
    assert '\nhealthcheck:\n  scale: 1' in health_platform

    overlay_version = _get_json(
        by_folder[('infra', 'ipsec-overlay')]['links']['defaultVersion'])
    overlay_files = overlay_version['files']
    overlay_docker = overlay_files['docker-compose.yml.tpl']
    overlay_platform = overlay_files['rancher-compose.yml']
    overlay_image = (
        'ghcr.io/pasturestack/ipsec-vxlan-overlay-network:v0.14.26')
    assert overlay_docker.count('image: {}'.format(overlay_image)) == 4
    assert '\n  overlay-network:\n' in overlay_docker
    assert '\n  overlay-router:\n' in overlay_docker
    assert '\n  connectivity-check:\n' in overlay_docker
    assert '\n  cni-driver:\n' in overlay_docker
    assert (
        'io.rancher.sidekicks: overlay-router,connectivity-check\n'
        in overlay_docker)
    assert 'connectivity-check,cni-driver' not in overlay_docker
    assert 'PASTURESTACK_NETWORK_XFRM_NETNS_PATH' in overlay_docker
    assert 'ipsec-vxlan-connectivity-check' in overlay_docker
    assert 'type: pasture-bridge' in overlay_docker
    assert 'type: metadata-cni-ipam' in overlay_docker
    assert 'pasture.internal' in overlay_docker
    assert 'RANCHER_' not in overlay_docker
    assert 'net.ipv4.conf.eth0.send_redirects' not in overlay_docker
    assert 'minimum_rancher_version: v1.6.19-rc1' in overlay_platform
    assert '\noverlay-network:\n  health_check:' in overlay_platform
    assert 'PSK' not in overlay_platform

    vxlan_version = _get_json(
        by_folder[('infra', 'vxlan-overlay-network')][
            'links']['defaultVersion'])
    vxlan_files = vxlan_version['files']
    vxlan_docker = vxlan_files['docker-compose.yml.tpl']
    vxlan_platform = vxlan_files['rancher-compose.yml']
    assert vxlan_docker.count('image: {}'.format(overlay_image)) == 3
    assert '\n  vxlan-network:\n' in vxlan_docker
    assert '\n  vxlan-router:\n' in vxlan_docker
    assert '\n  cni-driver:\n' in vxlan_docker
    assert 'command: start-vxlan.sh' in vxlan_docker
    assert '4789:4789/udp' in vxlan_docker
    assert 'io.rancher.sidekicks: vxlan-router' in vxlan_docker
    assert 'io.rancher.internal.service.vxlan' in vxlan_docker
    assert 'type: pasture-bridge' in vxlan_docker
    assert 'type: metadata-cni-ipam' in vxlan_docker
    assert 'pasture.internal' in vxlan_docker
    assert 'RANCHER_' not in vxlan_docker
    assert '@sha256:' not in vxlan_docker
    assert 'minimum_rancher_version: v1.6.11-rc1' in vxlan_platform

    layer_2_version = _get_json(
        by_folder[('infra', 'layer-2-flat-network')][
            'links']['defaultVersion'])
    layer_2_files = layer_2_version['files']
    layer_2_docker = layer_2_files['docker-compose.yml.tpl']
    layer_2_platform = layer_2_files['rancher-compose.yml']
    alternative_network_image = (
        'ghcr.io/pasturestack/ipsec-vxlan-overlay-network:v0.14.26')
    assert layer_2_docker.count(
        'image: {}'.format(alternative_network_image)) == 1
    assert '\n  layer-2-flat-cni:\n' in layer_2_docker
    assert 'command: start-cni-driver.sh' in layer_2_docker
    assert 'start-flat.sh && exec start-cni-driver.sh' in layer_2_docker
    assert 'io.rancher.network.cni.binary: pasture-bridge' in layer_2_docker
    assert 'type: pasture-bridge' in layer_2_docker
    assert 'type: flat-cni-ipam' in layer_2_docker
    assert 'metadataURL: http://169.254.169.250/2015-12-19' in (
        layer_2_docker)
    assert 'metadataAddress: 169.254.169.250' in layer_2_docker
    assert 'skipBridgeConfigureIP: true' in layer_2_docker
    assert 'AUTO_SETUP_LAYER_2_BRIDGE' in layer_2_docker
    assert 'RANCHER_' not in layer_2_docker
    assert '@sha256:' not in layer_2_docker
    assert 'minimum_rancher_version: v1.6.26-rc1' in layer_2_platform
    assert "default: 'false'" in layer_2_platform

    network_version = _get_json(
        by_folder[('infra', 'network-services')]['links']['defaultVersion'])
    network_files = network_version['files']
    network_docker = network_files['docker-compose.yml.tpl']
    network_platform = network_files['rancher-compose.yml']
    network_manager_image = (
        'ghcr.io/pasturestack/network-plugin-manager:v0.6.34')
    metadata_image = 'ghcr.io/pasturestack/metadata-service:v0.9.11'
    dns_image = 'ghcr.io/pasturestack/internal-dns:v0.17.11'
    assert network_docker.count(
        'image: {}'.format(network_manager_image)) == 1
    assert network_docker.count('image: {}'.format(metadata_image)) == 1
    assert network_docker.count('image: {}'.format(dns_image)) == 1
    assert '\n  network-plugin-manager:\n' in network_docker
    assert '\n  metadata:\n' in network_docker
    assert '\n  dns:\n' in network_docker
    assert 'network_mode: host' in network_docker
    assert 'network_mode: container:metadata' in network_docker
    assert '    user: root\n' in network_docker
    assert 'http://169.254.169.250/2016-07-29' in network_docker
    assert 'io.rancher.container.create_agent' in network_docker
    assert 'io.rancher.container.agent_service.metadata' in network_docker
    assert 'io.rancher.sidekicks: dns' in network_docker
    assert 'rancher-cni-driver:/etc/cni' in network_docker
    assert 'rancher-cni-driver:/opt/cni' in network_docker
    assert '$${CATTLE_URL:-}' in network_docker
    assert '$${CATTLE_ACCESS_KEY:-}' in network_docker
    assert '$${CATTLE_SECRET_KEY:-}' in network_docker
    assert '--disable-cni-setup' not in network_docker
    assert '--metadata-address' not in network_docker
    assert 'net.ipv4.conf.eth0.send_redirects' not in network_docker
    assert '/var/run:/var/run:ro' not in network_docker
    assert 'minimum_rancher_version: v1.6.26-rc1' in network_platform

    nfs_version = _get_json(
        by_folder[('infra', 'nfs-storage')]['links']['defaultVersion'])
    nfs_files = nfs_version['files']
    nfs_docker = nfs_files['docker-compose.yml']
    nfs_platform = nfs_files['rancher-compose.yml']
    nfs_image = 'ghcr.io/pasturestack/nfs-storage-driver:v0.10.0'
    assert nfs_docker.count('image: {}'.format(nfs_image)) == 1
    assert '\n  nfs-storage-driver:\n' in nfs_docker
    assert 'privileged: true' in nfs_docker
    assert 'network_mode: host' in nfs_docker
    assert "MOUNT_OPTS: '${MOUNT_OPTS},${NFS_VERS}'" in nfs_docker
    assert "ON_REMOVE: '${ON_REMOVE}'" in nfs_docker
    assert "PASTURESTACK_DEBUG: '${PASTURESTACK_DEBUG}'" in nfs_docker
    assert 'RANCHER_DEBUG' not in nfs_docker
    assert 'io.rancher.scheduler.global' in nfs_docker
    assert 'io.rancher.container.create_agent' in nfs_docker
    assert '/var/lib/rancher/volumes:/var/lib/pasturestack/volumes:shared' in (
        nfs_docker)
    assert 'minimum_rancher_version: v1.6.15-rc1' in nfs_platform
    assert 'default: retain' in nfs_platform
    assert '\nnfs-storage-driver:\n  storage_driver:' in nfs_platform
    assert 'name: pasturestack-nfs' in nfs_platform

    per_host_version = _get_json(
        by_folder[('infra', 'per-host-subnet-network')][
            'links']['defaultVersion'])
    per_host_files = per_host_version['files']
    per_host_docker = per_host_files['docker-compose.yml.tpl']
    per_host_platform = per_host_files['rancher-compose.yml']
    assert per_host_docker.count(
        'image: {}'.format(alternative_network_image)) == 2
    assert '\n  per-host-subnet-controller:\n' in per_host_docker
    assert '\n  per-host-subnet-cni:\n' in per_host_docker
    assert 'command: per-host-subnet' in per_host_docker
    assert 'PLATFORM_ROUTE_UPDATE_PROVIDER: host-gateway' in (
        per_host_docker)
    assert 'io.rancher.network.cni.binary: pasture-bridge' in per_host_docker
    assert 'type: pasture-bridge' in per_host_docker
    assert 'type: host-local-cni-ipam' in per_host_docker
    assert 'io.pasturestack.network.per-host-subnet.subnet' in (
        per_host_docker)
    assert 'io.pasturestack.network.per-host-subnet.range-start' in (
        per_host_docker)
    assert 'io.pasturestack.network.per-host-subnet.range-end' in (
        per_host_docker)
    assert 'dataDir: /opt/cni/state' in per_host_docker
    assert 'pasture.internal' in per_host_docker
    assert 'RANCHER_' not in per_host_docker
    assert '@sha256:' not in per_host_docker
    assert 'minimum_rancher_version: v1.6.26-rc1' in per_host_platform
    assert 'default: hostgw' not in per_host_platform

    scheduler_version = _get_json(
        by_folder[('infra', 'resource-scheduler')][
            'links']['defaultVersion'])
    scheduler_files = scheduler_version['files']
    scheduler_docker = scheduler_files['docker-compose.yml']
    scheduler_platform = scheduler_files['rancher-compose.yml']
    scheduler_image = 'ghcr.io/pasturestack/resource-scheduler:v0.8.15'
    assert scheduler_docker.count(
        'image: {}'.format(scheduler_image)) == 1
    assert '\n  resource-scheduler:\n' in scheduler_docker
    assert (
        'command: resource-scheduler --metadata-address 169.254.169.250'
        in scheduler_docker
    )
    assert "PASTURESTACK_DEBUG: '${PASTURESTACK_DEBUG}'" in scheduler_docker
    assert 'RANCHER_DEBUG' not in scheduler_docker
    assert '\nresource-scheduler:\n  health_check:' in scheduler_platform

    route53_version = _get_json(
        by_folder[('infra', 'route53-dns-sync')][
            'links']['defaultVersion'])
    route53_files = route53_version['files']
    route53_docker = route53_files['docker-compose.yml.tpl']
    route53_platform = route53_files['rancher-compose.yml']
    route53_image = 'ghcr.io/pasturestack/external-dns-sync:v0.8.0'
    assert route53_docker.count(
        'image: {}'.format(route53_image)) == 1
    assert '\n  route53-dns-sync:\n' in route53_docker
    assert '    command:\n      - -provider=route53\n' in route53_docker
    assert "io.rancher.container.agent.role: external-dns" in route53_docker
    assert "io.rancher.container.create_agent: 'true'" in route53_docker
    assert "AWS_ACCESS_KEY_ID: '${AWS_ACCESS_KEY_ID}'" in route53_docker
    assert "AWS_SECRET_ACCESS_KEY: '${AWS_SECRET_ACCESS_KEY}'" in (
        route53_docker)
    assert "AWS_SESSION_TOKEN: '${AWS_SESSION_TOKEN}'" in route53_docker
    assert "ROUTE53_ZONE_ID: '${ROUTE53_ZONE_ID}'" in route53_docker
    assert 'ROUTE53_ENDPOINT_URL' not in route53_docker
    assert '/var/lib/pasturestack/etc/ssl/ca.crt:ro' in route53_docker
    assert 'privileged: true' not in route53_docker
    assert '/var/run/docker.sock' not in route53_docker
    assert 'network_mode: host' not in route53_docker
    assert '@sha256:' not in route53_docker
    assert 'minimum_rancher_version: v1.6.13-rc1' in route53_platform
    assert route53_platform.count('type: password') == 2
    assert 'request_line: GET /ping HTTP/1.0' in route53_platform
    assert '\nroute53-dns-sync:\n  scale: 1' in route53_platform

    preloader_version = _get_json(
        by_folder[('infra', 'system-image-preloader')][
            'links']['defaultVersion'])
    preloader_files = preloader_version['files']
    preloader_docker = preloader_files['docker-compose.yml.tpl']
    preloader_platform = preloader_files['rancher-compose.yml']
    preloader_image = (
        'ghcr.io/pasturestack/system-image-preloader:v0.3.0')
    assert preloader_docker.count(
        'image: {}'.format(preloader_image)) == 1
    assert '\n  system-image-preloader:\n' in preloader_docker
    assert '/var/run/docker.sock:/var/run/docker.sock' in preloader_docker
    assert 'io.rancher.container.start_once' in preloader_docker
    assert 'io.rancher.container.create_agent' in preloader_docker
    assert "io.rancher.scheduler.global: 'true'" in preloader_docker
    assert "PLATFORM_VERSION: '${PLATFORM_VERSION}'" in preloader_docker
    assert 'IMAGE_PULL_MAX_ATTEMPTS' in preloader_docker
    assert 'CPU_WAIT_MAX_ATTEMPTS' in preloader_docker
    assert '{{- if' not in preloader_docker
    assert '{{- end' not in preloader_docker
    assert '@sha256:' not in preloader_docker
    assert 'ghcr.io/pasturestack/system-image-preloader:v0.3.0' in (
        preloader_docker)
    assert 'default: v1.6.282' in preloader_platform
    assert 'default: false' in preloader_platform
    assert '\nsystem-image-preloader:\n  start_on_create: true' in (
        preloader_platform)

    project_version = _get_json(
        by_folder[('project', 'native')]['links']['defaultVersion'])
    project_files = project_version['files']
    project = project_files['project.yml']
    project_platform = project_files['rancher-compose.yml']
    assert 'name: PastureStack Native' in project
    assert "templateId: 'pasturestack:infra*network-services'" in project
    assert "templateId: 'pasturestack:infra*ipsec-overlay'" in project
    assert "templateId: 'pasturestack:infra*resource-scheduler'" in project
    assert "templateId: 'pasturestack:infra*healthcheck'" in project
    assert '.catalog:\n  name: PastureStack Native' in project_platform


def test_catalog_commit_is_pinned():
    catalogs = _get_json('http://localhost:8088/v1-catalog/catalogs')
    data = catalogs.get('data', [])
    assert len(data) == 1
    assert data[0]['branch'] == _current_branch()
    assert data[0]['pinnedCommit'] == _catalog_commit()
