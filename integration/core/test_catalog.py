import json
import os
import re
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


def _catalog_url(path):
    base = os.environ.get(
        'CATALOG_TEST_BASE_URL', 'http://localhost:8088').rstrip('/')
    return '{}/{}'.format(base, path.lstrip('/'))


def _catalog_name():
    return os.environ.get('CATALOG_TEST_NAME', 'library')


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
    templates = _get_json(_catalog_url('/v1-catalog/templates'))
    data = templates.get('data', [])
    assert len(data) == 22
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
        ('infra', 'network-diagnostics'),
        ('infra', 'network-policy-manager'),
        ('infra', 'network-services'),
        ('infra', 'nfs-storage'),
        ('infra', 'secret-volume-driver'),
        ('infra', 'per-host-subnet-network'),
        ('infra', 'resource-scheduler'),
        ('infra', 'route53-dns-sync'),
        ('infra', 'system-image-preloader'),
        ('infra', 'vault-volume-driver'),
        ('infra', 'vxlan-overlay-network'),
        ('infra', 'windows-container-networking'),
        ('infra', 'windows-ecr-credential-sync'),
        ('infra', 'windows-network-services'),
        ('project', 'native'),
    }
    for template in by_folder.values():
        assert not template['name'].casefold().startswith('pasturestack ')
        assert re.fullmatch(r'v\d+\.\d+\.\d+', template['defaultVersion'])
        localized_name = template.get('labels', {}).get(
            'io.pasturestack.catalog.name.zh-tw', '')
        assert not localized_name.casefold().startswith('pasturestack ')

    assert by_folder[('infra', 'amazon-ebs-storage')][
        'name'] == 'Amazon EBS Storage'
    assert by_folder[('infra', 'amazon-ebs-storage')][
        'defaultVersion'] == 'v0.11.1'
    assert by_folder[('infra', 'amazon-ebs-storage')][
        'links']['defaultVersion'].endswith(
        ':3')
    assert by_folder[('infra', 'amazon-efs-storage')][
        'name'] == 'Amazon EFS Storage'
    assert by_folder[('infra', 'amazon-efs-storage')][
        'defaultVersion'] == 'v0.11.1'
    assert by_folder[('infra', 'amazon-efs-storage')][
        'links']['defaultVersion'].endswith(
        ':3')
    assert by_folder[('infra', 'container-schedule')][
        'name'] == 'Container Schedule'
    assert by_folder[('infra', 'container-schedule')][
        'defaultVersion'] == 'v0.6.2'
    assert by_folder[('infra', 'container-schedule')][
        'links']['defaultVersion'].endswith(
        ':4')
    assert by_folder[('infra', 'ecr-credential-sync')][
        'name'] == 'Amazon ECR Credential Sync'
    assert by_folder[('infra', 'ecr-credential-sync')][
        'defaultVersion'] == 'v3.1.6'
    assert by_folder[('infra', 'ecr-credential-sync')][
        'links']['defaultVersion'].endswith(
        ':4')
    assert by_folder[('infra', 'healthcheck')][
        'name'] == 'Metadata Healthcheck'
    assert by_folder[('infra', 'healthcheck')][
        'defaultVersion'] == 'v0.3.18'
    assert by_folder[('infra', 'healthcheck')][
        'links']['defaultVersion'].endswith(
        ':3')
    assert by_folder[('infra', 'ipsec-overlay')]['name'] == (
        'IPsec Overlay')
    assert by_folder[('infra', 'ipsec-overlay')][
        'defaultVersion'] == 'v0.3.12'
    assert by_folder[('infra', 'ipsec-overlay')][
        'links']['defaultVersion'].endswith(
        ':14')
    assert by_folder[('infra', 'layer-2-flat-network')]['name'] == (
        'Layer 2 Flat Network')
    assert by_folder[('infra', 'layer-2-flat-network')][
        'defaultVersion'] == 'v0.3.6'
    assert by_folder[('infra', 'layer-2-flat-network')][
        'links']['defaultVersion'].endswith(
        ':8')
    assert by_folder[('infra', 'network-diagnostics')]['name'] == (
        'Network Diagnostics')
    assert by_folder[('infra', 'network-diagnostics')][
        'defaultVersion'] == 'v0.2.2'
    assert by_folder[('infra', 'network-diagnostics')][
        'links']['defaultVersion'].endswith(
        ':3')
    assert by_folder[('infra', 'network-policy-manager')]['name'] == (
        'Network Policy Manager')
    assert by_folder[('infra', 'network-policy-manager')][
        'defaultVersion'] == 'v0.3.5'
    assert by_folder[('infra', 'network-policy-manager')][
        'links']['defaultVersion'].endswith(
        ':5')
    assert by_folder[('infra', 'network-services')]['name'] == (
        'Network Services')
    assert by_folder[('infra', 'network-services')][
        'defaultVersion'] == 'v0.3.12'
    assert by_folder[('infra', 'network-services')][
        'links']['defaultVersion'].endswith(
        ':14')
    assert by_folder[('infra', 'nfs-storage')][
        'name'] == 'NFS Storage'
    assert by_folder[('infra', 'nfs-storage')][
        'defaultVersion'] == 'v0.11.1'
    assert by_folder[('infra', 'nfs-storage')][
        'links']['defaultVersion'].endswith(
        ':3')
    assert by_folder[('infra', 'secret-volume-driver')][
        'name'] == 'Secret Volume'
    assert by_folder[('infra', 'secret-volume-driver')][
        'defaultVersion'] == 'v0.1.4'
    assert by_folder[('infra', 'secret-volume-driver')][
        'links']['defaultVersion'].endswith(
        ':4')
    assert by_folder[('infra', 'vault-volume-driver')][
        'name'] == 'Vault Volume'
    assert by_folder[('infra', 'vault-volume-driver')][
        'defaultVersion'] == 'v0.2.3'
    assert by_folder[('infra', 'vault-volume-driver')][
        'links']['defaultVersion'].endswith(
        ':5')
    assert by_folder[('infra', 'per-host-subnet-network')]['name'] == (
        'Per-Host Subnet Network')
    assert by_folder[('infra', 'per-host-subnet-network')][
        'defaultVersion'] == 'v0.3.4'
    assert by_folder[('infra', 'per-host-subnet-network')][
        'links']['defaultVersion'].endswith(':6')
    assert by_folder[('infra', 'resource-scheduler')][
        'name'] == 'Resource Scheduler'
    assert by_folder[('infra', 'resource-scheduler')][
        'defaultVersion'] == 'v0.8.21'
    assert by_folder[('infra', 'resource-scheduler')][
        'links']['defaultVersion'].endswith(
        ':7')
    assert by_folder[('infra', 'route53-dns-sync')][
        'name'] == 'Route 53 DNS Sync'
    assert by_folder[('infra', 'route53-dns-sync')][
        'defaultVersion'] == 'v0.8.1'
    assert by_folder[('infra', 'route53-dns-sync')][
        'links']['defaultVersion'].endswith(
        ':3')
    assert by_folder[('infra', 'system-image-preloader')]['name'] == (
        'System Image Preloader')
    assert by_folder[('infra', 'system-image-preloader')][
        'defaultVersion'] == 'v0.3.3'
    assert by_folder[('infra', 'system-image-preloader')][
        'links']['defaultVersion'].endswith(
        ':4')
    assert by_folder[('infra', 'vxlan-overlay-network')]['name'] == (
        'VXLAN Overlay Network')
    assert by_folder[('infra', 'vxlan-overlay-network')][
        'defaultVersion'] == 'v0.3.5'
    assert by_folder[('infra', 'vxlan-overlay-network')][
        'links']['defaultVersion'].endswith(
        ':7')
    assert by_folder[('infra', 'windows-container-networking')][
        'name'] == 'Windows Container Networking'
    assert by_folder[('infra', 'windows-container-networking')][
        'defaultVersion'] == 'v0.1.2'
    assert by_folder[('infra', 'windows-container-networking')][
        'links']['defaultVersion'].endswith(
        ':4')
    assert by_folder[('infra', 'windows-ecr-credential-sync')][
        'name'] == 'Windows ECR Credential Sync'
    assert by_folder[('infra', 'windows-ecr-credential-sync')][
        'defaultVersion'] == 'v3.1.2'
    assert by_folder[('infra', 'windows-ecr-credential-sync')][
        'links']['defaultVersion'].endswith(
        ':2')
    assert by_folder[('infra', 'windows-network-services')][
        'name'] == 'Windows Network Services'
    assert by_folder[('infra', 'windows-network-services')][
        'defaultVersion'] == 'v0.3.0'
    assert by_folder[('infra', 'windows-network-services')][
        'links']['defaultVersion'].endswith(
        ':2')
    assert by_folder[('project', 'native')][
        'name'] == 'Native'
    assert by_folder[('project', 'native')][
        'defaultVersion'] == 'v0.3.0'
    localized = {
        ('infra', 'amazon-ebs-storage'): (
            'Amazon EBS 儲存空間',
            '掛載既有的 Amazon EBS 磁碟區；如需建立加密磁碟區，必須明確啟用雲端資源配置。'),
        ('infra', 'amazon-efs-storage'): (
            'Amazon EFS 儲存空間',
            '掛載既有的 Amazon EFS 檔案系統；如需建立檔案系統與掛載目標，必須明確啟用雲端資源配置。'),
        ('infra', 'container-schedule'): (
            '容器定時排程',
            '依容器標籤中的 Cron 表達式，定時啟動、停止或重新啟動容器。'),
        ('infra', 'ecr-credential-sync'): (
            'Amazon ECR 登入資訊同步',
            '定期更新 Amazon Elastic Container Registry 的短效登入資訊，並同步至目前或指定的環境。'),
        ('infra', 'healthcheck'): (
            '中繼資料健康檢查',
            '依據中繼資料定義檢查工作負載健康狀態，並透過相容控制 API 回報結果。'),
        ('infra', 'ipsec-overlay'): (
            'IPsec 加密網路',
            '為受管工作負載提供跨主機的加密網路。'),
        ('infra', 'layer-2-flat-network'): (
            '第 2 層平面網路',
            '透過主機網橋，將受管理的工作負載直接連接到共用的第 2 層子網路。'),
        ('infra', 'network-diagnostics'): (
            '網路診斷',
            '蒐集經過界線控管與去識別化處理的主機網路健康摘要，並保留由管理者建立的診斷封存檔。'),
        ('infra', 'network-policy-manager'): (
            '網路政策管理器',
            '依中繼資料中的網路政策，在每台受管主機套用最小權限的流量控管規則。'),
        ('infra', 'network-services'): (
            '網路服務',
            '安裝受管工作負載所需的主機網路、中繼資料與內部 DNS 服務。'),
        ('infra', 'nfs-storage'): (
            'NFS 儲存空間',
            '提供 NFS 第 3 版與第 4 版的 Docker 磁碟區，移除磁碟區時預設保留資料。'),
        ('infra', 'secret-volume-driver'): (
            '機密資料磁碟區',
            '將控制平面核准的加密機密資料，以唯讀的記憶體磁碟區安全提供給工作負載。'),
        ('infra', 'vault-volume-driver'): (
            'Vault 存取權杖磁碟區',
            '透過主機身分驗證及唯讀記憶體磁碟區，為每個工作負載安全提供短效、回應封裝的 Vault 存取權杖。'),
        ('infra', 'per-host-subnet-network'): (
            '每台主機獨立子網路',
            '為每台主機配置獨立的工作負載子網路，並維護主機間的閘道路由。'),
        ('infra', 'resource-scheduler'): (
            '資源排程器',
            '依控制平面事件與目前的中繼資料狀態，排程原生工作負載。'),
        ('infra', 'route53-dns-sync'): (
            'Route 53 DNS 紀錄同步',
            '將相容環境的服務位址同步至指定的 Amazon Route 53 託管區域。'),
        ('infra', 'system-image-preloader'): (
            '系統映像預先下載',
            '預先下載相容基礎架構堆疊所需的容器映像，以縮短主機升級等待時間。'),
        ('infra', 'vxlan-overlay-network'): (
            'VXLAN 覆疊網路',
            '透過 UDP 4789，在受管主機之間建立未加密的 VXLAN 覆疊網路。'),
        ('infra', 'windows-container-networking'): (
            'Windows 容器網路',
            '為相容的 Windows 容器主機定義 NAT 與透明 Docker 網路驅動程式。'),
        ('infra', 'windows-ecr-credential-sync'): (
            'Windows ECR 登入資訊同步',
            '從相容的 Windows Server 2022 主機定期更新 Amazon ECR 短效登入資訊。'),
        ('infra', 'windows-network-services'): (
            'Windows 網路服務',
            '為相容的 Windows Server 2022 工作負載安裝中繼資料與內部 DNS 服務。'),
        ('project', 'native'): (
            '原生專案範本',
            'PastureStack 原生編排執行環境的預設專案範本。'),
    }
    for key, (name, description) in localized.items():
        labels = by_folder[key]['labels']
        assert labels['io.pasturestack.catalog.name.zh-tw'] == name
        assert labels[
            'io.pasturestack.catalog.description.zh-tw'] == description

    with open(_file('catalog-provenance.json'), encoding='utf-8') as source:
        provenance = json.load(source)
    assert provenance['classification'] == 'upstream-first-party'
    assert len(provenance['entries']) == 21
    localized_question_count = 0
    for folder, origin in provenance['entries'].items():
        template = by_folder[('infra', folder)]
        labels = template['labels']
        assert labels[
            'io.pasturestack.catalog.origin'] == 'upstream-first-party'
        assert labels[
            'io.pasturestack.catalog.origin-template'] == (
                origin['sourcePath'].rsplit('/', 1)[-1])
        assert labels[
            'io.pasturestack.catalog.origin-status'] == origin['originStatus']

        version = _get_json(template['links']['defaultVersion'])
        files = version['files']
        assert files['README.zh-TW.md'].strip()
        compose = files.get('rancher-compose.yml', '')
        variables = re.findall(
            r'^\s*-\s+variable:\s*[\'"]?([A-Za-z0-9_]+)',
            compose,
            re.MULTILINE)
        localized_question_count += len(variables)
        for variable in variables:
            prefix = (
                'io.pasturestack.catalog.question.{}'
                .format(variable.lower()))
            assert '{}.label.zh-tw:'.format(prefix) in compose
            assert '{}.description.zh-tw:'.format(prefix) in compose
    assert localized_question_count == 142


def test_catalog_compose_shapes_are_runtime_compatible():
    templates = _get_json(_catalog_url('/v1-catalog/templates'))
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
    ebs_image = 'ghcr.io/pasturestack/ebs-storage-driver:v0.11.1'
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
    efs_image = 'ghcr.io/pasturestack/efs-storage-driver:v0.11.1'
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
        'ghcr.io/pasturestack/container-cron:v0.6.2')
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
    ecr_image = 'ghcr.io/pasturestack/ecr-credential-sync:v3.1.6'
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
    health_image = 'ghcr.io/pasturestack/metadata-healthcheck:v0.3.18'
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
        'ghcr.io/pasturestack/ipsec-vxlan-overlay-network:v0.14.41')
    assert overlay_docker.count('image: {}'.format(overlay_image)) == 4
    assert overlay_docker.count(
        "PASTURESTACK_FIREWALL_BACKEND: '${FIREWALL_BACKEND}'") == 1
    assert overlay_platform.count('variable: FIREWALL_BACKEND') == 1
    assert 'default: auto' in overlay_platform
    for backend in ('nftables', 'iptables-nft', 'iptables-legacy'):
        assert '\n    - {}'.format(backend) in overlay_platform
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
    assert 'allowSharedSubnetIngress: true' in overlay_docker
    assert 'type: metadata-cni-ipam' in overlay_docker
    assert 'pasture.internal' in overlay_docker
    assert 'RANCHER_' not in overlay_docker
    assert 'net.ipv4.conf.eth0.send_redirects' not in overlay_docker
    assert 'minimum_rancher_version: v1.6.19-rc1' in overlay_platform
    assert '\noverlay-network:\n  health_check:' in overlay_platform
    assert 'PSK' not in overlay_platform

    retained_overlay = _get_json(_catalog_url(
        '/v1-catalog/templateversions/{}:infra*ipsec-overlay:11'.format(
            _catalog_name())))
    assert retained_overlay['files']['docker-compose.yml.tpl'].count(
        'image: ghcr.io/pasturestack/ipsec-vxlan-overlay-network:v0.14.35'
    ) == 4

    vxlan_version = _get_json(
        by_folder[('infra', 'vxlan-overlay-network')][
            'links']['defaultVersion'])
    vxlan_files = vxlan_version['files']
    vxlan_docker = vxlan_files['docker-compose.yml.tpl']
    vxlan_platform = vxlan_files['rancher-compose.yml']
    alternative_network_image = (
            'ghcr.io/pasturestack/ipsec-vxlan-overlay-network:v0.14.41')
    assert vxlan_docker.count(
        'image: {}'.format(alternative_network_image)) == 3
    assert '\n  vxlan-network:\n' in vxlan_docker
    assert '\n  vxlan-router:\n' in vxlan_docker
    assert '\n  cni-driver:\n' in vxlan_docker
    assert 'command: start-vxlan.sh' in vxlan_docker
    assert '4789:4789/udp' in vxlan_docker
    assert 'io.rancher.sidekicks: vxlan-router' in vxlan_docker
    assert 'io.rancher.internal.service.vxlan' in vxlan_docker
    assert 'type: pasture-bridge' in vxlan_docker
    assert 'allowSharedSubnetIngress: true' in vxlan_docker
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
    flat_network_image = (
        'ghcr.io/pasturestack/ipsec-vxlan-overlay-network:v0.14.41')
    assert layer_2_docker.count(
        'image: {}'.format(flat_network_image)) == 1
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

    diagnostics_version = _get_json(
        by_folder[('infra', 'network-diagnostics')][
            'links']['defaultVersion'])
    diagnostics_files = diagnostics_version['files']
    diagnostics_docker = diagnostics_files['docker-compose.yml.tpl']
    diagnostics_platform = diagnostics_files['rancher-compose.yml']
    diagnostics_agent_image = (
        'ghcr.io/pasturestack/network-diagnostics-agent:v0.2.1')
    diagnostics_service_image = (
        'ghcr.io/pasturestack/network-diagnostics-service:v0.2.1')
    assert diagnostics_docker.count(
        'image: {}'.format(diagnostics_agent_image)) == 1
    assert diagnostics_docker.count(
        'image: {}'.format(diagnostics_service_image)) == 1
    assert '\n  network-diagnostics-service:\n' in diagnostics_docker
    assert '\n  network-diagnostics-agent:\n' in diagnostics_docker
    assert "io.rancher.scheduler.global: 'true'" in diagnostics_docker
    assert '/proc:/host/proc:ro' in diagnostics_docker
    assert '/etc/resolv.conf:/host/etc/resolv.conf:ro' in diagnostics_docker
    assert '/etc/machine-id:/host/etc/machine-id:ro' in diagnostics_docker
    assert 'network-diagnostics-data:' in diagnostics_docker
    assert "'${PUBLISHED_PORT}:8080/tcp'" in diagnostics_docker
    assert 'privileged: true' not in diagnostics_docker
    assert 'network_mode: host' not in diagnostics_docker
    assert '/var/run/docker.sock' not in diagnostics_docker
    assert '@sha256:' not in diagnostics_docker
    assert 'minimum_rancher_version: v1.6.13-rc1' in diagnostics_platform
    assert 'variable: COLLECTION_TOKEN' in diagnostics_platform
    assert diagnostics_platform.count('type: password') == 1
    assert 'default: 8091' in diagnostics_platform
    assert (
        '\nnetwork-diagnostics-service:\n  scale: 1\n'
        in diagnostics_platform)
    assert (
        '\nnetwork-diagnostics-agent:\n  start_on_create: true\n'
        in diagnostics_platform)
    assert diagnostics_platform.count(
        'request_line: GET /healthz HTTP/1.0') == 2

    policy_version = _get_json(
        by_folder[('infra', 'network-policy-manager')][
            'links']['defaultVersion'])
    policy_files = policy_version['files']
    policy_docker = policy_files['docker-compose.yml']
    policy_platform = policy_files['rancher-compose.yml']
    policy_image = (
        'ghcr.io/pasturestack/network-policy-manager:v0.3.3')
    assert policy_docker.count(
        'image: {}'.format(policy_image)) == 1
    assert '\n  network-policy-manager:\n' in policy_docker
    assert 'network_mode: host' in policy_docker
    assert "io.rancher.scheduler.global: 'true'" in policy_docker
    assert 'cap_drop:\n      - ALL' in policy_docker
    assert 'cap_add:\n      - NET_ADMIN' in policy_docker
    assert 'read_only: true' in policy_docker
    assert '/tmp:rw,noexec,nosuid,size=8m' in policy_docker
    assert 'no-new-privileges:true' in policy_docker
    assert '--cleanup-on-exit' in policy_docker
    assert '--fail-open-after' in policy_docker
    assert '/var/run/docker.sock' not in policy_docker
    assert 'privileged: true' not in policy_docker
    assert 'pid: host' not in policy_docker
    assert '@sha256:' not in policy_docker
    assert 'minimum_rancher_version: v1.6.26-rc1' in policy_platform
    assert '--health-listen' in policy_docker
    assert 'health_check:' not in policy_platform
    assert 'port: 8092' not in policy_platform

    network_version = _get_json(
        by_folder[('infra', 'network-services')]['links']['defaultVersion'])
    network_files = network_version['files']
    network_docker = network_files['docker-compose.yml.tpl']
    network_platform = network_files['rancher-compose.yml']
    network_manager_image = (
        'ghcr.io/pasturestack/network-plugin-manager:v0.8.25')
    metadata_image = 'ghcr.io/pasturestack/metadata-service:v0.10.7'
    dns_image = 'ghcr.io/pasturestack/internal-dns:v0.17.14'
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
    assert '/run:/run' in network_docker
    assert network_docker.count('--firewall-backend') == 1
    assert network_docker.count('${FIREWALL_BACKEND}') == 1
    assert network_platform.count('variable: FIREWALL_BACKEND') == 1
    assert 'default: auto' in network_platform
    for backend in ('nftables', 'iptables-nft', 'iptables-legacy'):
        assert '\n    - {}'.format(backend) in network_platform
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
    nfs_image = 'ghcr.io/pasturestack/nfs-storage-driver:v0.11.1'
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

    secret_version = _get_json(
        by_folder[('infra', 'secret-volume-driver')][
            'links']['defaultVersion'])
    secret_files = secret_version['files']
    secret_docker = secret_files['docker-compose.yml']
    secret_platform = secret_files['rancher-compose.yml']
    secret_image = (
        'ghcr.io/pasturestack/secrets-flexvolume-plugin:v0.2.2')
    assert secret_docker.count('image: {}'.format(secret_image)) == 1
    assert '\n  secret-volume-driver:\n' in secret_docker
    assert 'privileged:' not in secret_docker
    assert 'network_mode:' not in secret_docker
    assert '/var/run/docker.sock' not in secret_docker
    assert '\n    cap_drop:\n    - ALL\n' in secret_docker
    assert (
        '\n    cap_add:\n    - SYS_ADMIN\n    - CHOWN\n    - FOWNER\n'
        in secret_docker)
    assert 'read_only: true' in secret_docker
    assert 'apparmor:unconfined' in secret_docker
    assert 'no-new-privileges:true' in secret_docker
    assert (
        'io.rancher.container.agent.role: environment,agent'
        in secret_docker)
    assert '@sha256:' not in secret_docker
    assert (
        '/var/lib/rancher/etc/ssl/host.key:'
        '/var/lib/pasturestack/etc/ssl/host.key:ro' in secret_docker)
    assert (
        '/var/lib/pasturestack/volumes:'
        '/var/lib/pasturestack/volumes:shared' in secret_docker)
    assert 'minimum_rancher_version: v1.6.15-rc1' in secret_platform
    assert '\nsecret-volume-driver:\n  storage_driver:' in secret_platform
    assert 'name: pasturestack-secret-volume' in secret_platform
    assert 'volume_capabilities:\n    - secrets' in secret_platform
    assert 'strategy: none' in secret_platform

    vault_version = _get_json(
        by_folder[('infra', 'vault-volume-driver')][
            'links']['defaultVersion'])
    vault_files = vault_version['files']
    vault_labels = vault_version['labels']
    vault_docker = vault_files['docker-compose.yml']
    vault_platform = vault_files['rancher-compose.yml']
    assert '# PastureStack Vault 存取權杖磁碟區' in (
        vault_files['README.zh-TW.md'])
    assert vault_labels[
        'io.pasturestack.catalog.question.vault_url.label.zh-tw'
    ] == 'Vault API 網址'
    assert vault_labels[
        'io.pasturestack.catalog.question.vault_role.label.zh-tw'
    ] == 'Vault 權杖角色'
    assert vault_labels[
        'io.pasturestack.catalog.question.'
        'vault_allowed_policies.label.zh-tw'
    ] == '允許的 Vault 存取政策'
    assert vault_labels[
        'io.pasturestack.catalog.question.'
        'issuing_token_secret.label.zh-tw'
    ] == 'Vault 發行用權杖機密資料'
    vault_bridge_image = (
        'ghcr.io/pasturestack/vault-secrets-bridge:v0.1.3')
    vault_driver_image = (
        'ghcr.io/pasturestack/secrets-flexvolume-plugin:v0.2.2')
    assert vault_docker.count(
        'image: {}'.format(vault_bridge_image)) == 1
    assert vault_docker.count(
        'image: {}'.format(vault_driver_image)) == 1
    assert '\n  vault-secrets-bridge:\n' in vault_docker
    assert '\n  vault-volume-driver:\n' in vault_docker
    assert 'PASTURESTACK_VAULT_ISSUER_TOKEN_FILE:' in vault_docker
    assert '/run/secrets/{{.Values.ISSUING_TOKEN_SECRET}}' in vault_docker
    assert '\n      VAULT_TOKEN:' not in vault_docker
    assert '\n      PASTURESTACK_VAULT_ISSUER_TOKEN:' not in vault_docker
    assert 'PASTURESTACK_SECRET_PROVIDER: vault' in vault_docker
    assert (
        'PASTURESTACK_VAULT_BRIDGE_URL: '
        'http://vault-secrets-bridge:8080' in vault_docker)
    assert 'privileged:' not in vault_docker
    assert 'network_mode:' not in vault_docker
    assert '/var/run/docker.sock' not in vault_docker
    assert vault_docker.count('\n    cap_drop:\n    - ALL\n') == 2
    assert (
        '\n    cap_add:\n    - SYS_ADMIN\n    - CHOWN\n    - FOWNER\n'
        in vault_docker)
    assert vault_docker.count('read_only: true') == 2
    assert 'apparmor:unconfined' in vault_docker
    assert vault_docker.count('no-new-privileges:true') == 2
    assert (
        '/var/lib/rancher/etc/ssl/host.key:'
        '/var/lib/pasturestack/etc/ssl/host.key:ro' in vault_docker)
    assert 'vault-secrets-bridge-state:' in vault_docker
    assert '@sha256:' not in vault_docker
    assert 'minimum_rancher_version: v1.6.15-rc1' in vault_platform
    assert 'variable: ISSUING_TOKEN_SECRET' in vault_platform
    assert 'type: secret' in vault_platform
    assert '\nvault-secrets-bridge:\n  scale: 1' in vault_platform
    assert '\nvault-volume-driver:\n  storage_driver:' in vault_platform
    assert 'name: pasturestack-vault-volume' in vault_platform
    assert vault_platform.count(
        'request_line: GET /readyz HTTP/1.0') == 2
    assert vault_platform.count('strategy: none') == 2

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
    scheduler_image = 'ghcr.io/pasturestack/resource-scheduler:v0.8.21'
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
    route53_image = 'ghcr.io/pasturestack/external-dns-sync:v0.8.1'
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
        'ghcr.io/pasturestack/system-image-preloader:v0.3.3')
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
    assert 'ghcr.io/pasturestack/system-image-preloader:v0.3.3' in (
        preloader_docker)
    assert 'default: v1.6.282' in preloader_platform
    assert 'default: false' in preloader_platform
    assert '\nsystem-image-preloader:\n  start_on_create: true' in (
        preloader_platform)

    windows_ecr_version = _get_json(
        by_folder[('infra', 'windows-ecr-credential-sync')][
            'links']['defaultVersion'])
    windows_ecr_files = windows_ecr_version['files']
    windows_ecr_docker = windows_ecr_files['docker-compose.yml.tpl']
    windows_ecr_platform = windows_ecr_files['rancher-compose.yml']
    windows_ecr_image = (
        'ghcr.io/pasturestack/ecr-credential-sync-windows:'
        'v3.1.2')
    assert windows_ecr_docker.count(
        'image: {}'.format(windows_ecr_image)) == 1
    assert 'io.rancher.host.os=windows' in windows_ecr_docker
    assert "io.rancher.container.create_agent: 'true'" in (
        windows_ecr_docker)
    assert "PLATFORM_URL: '${PLATFORM_URL}'" in windows_ecr_docker
    assert '@sha256:' not in windows_ecr_docker
    assert '# PastureStack Windows ECR 登入資訊同步' in (
        windows_ecr_files['README.zh-TW.md'])
    assert windows_ecr_version['labels'][
        'io.pasturestack.catalog.question.aws_region.label.zh-tw'
    ] == 'AWS 區域'
    assert windows_ecr_version['labels'][
        'io.pasturestack.catalog.question.log_level.label.zh-tw'
    ] == '日誌詳細程度'
    assert 'minimum_rancher_version: v1.6.15-rc1' in (
        windows_ecr_platform)

    windows_network_version = _get_json(
        by_folder[('infra', 'windows-network-services')][
            'links']['defaultVersion'])
    windows_network_files = windows_network_version['files']
    windows_network_docker = windows_network_files['docker-compose.yml.tpl']
    windows_network_platform = windows_network_files['rancher-compose.yml']
    windows_metadata_image = (
        'ghcr.io/pasturestack/metadata-service-windows:'
        'v0.9.12')
    windows_dns_image = (
        'ghcr.io/pasturestack/internal-dns-windows:'
        'v0.17.12')
    assert windows_network_docker.count(
        'image: {}'.format(windows_metadata_image)) == 1
    assert windows_network_docker.count(
        'image: {}'.format(windows_dns_image)) == 1
    assert windows_network_docker.count(
        'io.rancher.host.os=windows') == 2
    assert '--metadata-url=http://169.254.169.250/2016-07-29' in (
        windows_network_docker)
    assert '--answers=C:\\pasturestack\\answers.json' in (
        windows_network_docker)
    assert '@sha256:' not in windows_network_docker
    assert '# PastureStack Windows 網路服務' in (
        windows_network_files['README.zh-TW.md'])
    assert windows_network_version['labels'][
        'io.pasturestack.catalog.question.'
        'dns_recurser_timeout.label.zh-tw'
    ] == 'DNS 遞迴查詢逾時'
    assert windows_network_version['labels'][
        'io.pasturestack.catalog.question.ttl.label.zh-tw'
    ] == '服務探索 DNS 記錄存留時間'
    assert 'minimum_rancher_version: v1.6.15-rc1' in (
        windows_network_platform)

    windows_container_network_version = _get_json(
        by_folder[('infra', 'windows-container-networking')][
            'links']['defaultVersion'])
    windows_container_network_files = (
        windows_container_network_version['files'])
    windows_container_network_docker = (
        windows_container_network_files['docker-compose.yml'])
    windows_container_network_platform = (
        windows_container_network_files['rancher-compose.yml'])
    selector_image = (
        'ghcr.io/pasturestack/pod-pause-image:'
        'v3.0.6')
    assert windows_container_network_docker.count(
        'image: {}'.format(selector_image)) == 2
    assert windows_container_network_docker.count(
        'io.rancher.service.selector.container: '
        'experimental-windows-rancher') == 2
    assert 'image: rancher/none' not in windows_container_network_docker
    assert '@sha256:' not in windows_container_network_docker
    assert '# PastureStack Windows 容器網路' in (
        windows_container_network_files['README.zh-TW.md'])
    assert 'kind: nat' in windows_container_network_platform
    assert 'kind: $TRANSPARENT_NETWORK_DRIVER_NAME' in (
        windows_container_network_platform)
    assert windows_container_network_version['labels'][
        'io.pasturestack.catalog.question.'
        'transparent_network_driver_name.label.zh-tw'
    ] == '透明網路驅動程式名稱'

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


@pytest.mark.parametrize(
    'template,old_number,new_number,old_version,new_version,replacements', [
        (
            'network-diagnostics', '2', '3',
            'v0.2.1', 'v0.2.2', [
                (
                    'network-diagnostics-agent:v0.2.0',
                    'network-diagnostics-agent:v0.2.1',
                ),
                (
                    'network-diagnostics-service:v0.2.0',
                    'network-diagnostics-service:v0.2.1',
                ),
            ],
        ),
        (
            'healthcheck', '1', '2',
            'v0.3.16', 'v0.3.17', [
                (
                    'metadata-healthcheck:v0.3.16',
                    'metadata-healthcheck:v0.3.17',
                ),
            ],
        ),
        (
            'secret-volume-driver', '2', '3',
            'v0.1.2', 'v0.1.3', [
                (
                    'secrets-flexvolume-plugin:v0.1.1',
                    'secrets-flexvolume-plugin:v0.2.1',
                ),
            ],
        ),
        (
            'vault-volume-driver', '3', '4',
            'v0.2.1', 'v0.2.2', [
                (
                    'vault-secrets-bridge:v0.1.1',
                    'vault-secrets-bridge:v0.1.2',
                ),
                (
                    'secrets-flexvolume-plugin:v0.2.0',
                    'secrets-flexvolume-plugin:v0.2.1',
                ),
            ],
        ),
        (
            'windows-container-networking', '2', '3',
            'v0.1.0', 'v0.1.1', [
                (
                    'pod-pause-image:v3.0.2',
                    'pod-pause-image:v3.0.5',
                ),
            ],
        ),
        (
            'network-services', '12', '13',
            'v0.3.10', 'v0.3.11', [
                (
                    'network-plugin-manager:v0.8.24',
                    'network-plugin-manager:v0.8.25',
                ),
                (
                    'metadata-service:v0.10.5',
                    'metadata-service:v0.10.6',
                ),
            ],
        ),
        (
            'network-services', '11', '12',
            'v0.3.9', 'v0.3.10', [
                (
                    'network-plugin-manager:v0.8.23',
                    'network-plugin-manager:v0.8.24',
                ),
            ],
        ),
        (
            'network-services', '10', '11',
            'v0.3.8', 'v0.3.9', [
                (
                    'network-plugin-manager:v0.8.22',
                    'network-plugin-manager:v0.8.23',
                ),
                (
                    'metadata-service:v0.9.11',
                    'metadata-service:v0.10.5',
                ),
                (
                    'internal-dns:v0.17.11',
                    'internal-dns:v0.17.13',
                ),
            ],
        ),
        (
            'network-policy-manager', '3', '4',
            'v0.3.3', 'v0.3.4', [
                (
                    'network-policy-manager:v0.3.1',
                    'network-policy-manager:v0.3.2',
                ),
            ],
        ),
        (
            'system-image-preloader', '2', '3',
            'v0.3.0', 'v0.3.2', [
                (
                    'system-image-preloader:v0.3.0',
                    'system-image-preloader:v0.3.2',
                ),
            ],
        ),
        (
            'route53-dns-sync', '2', '3',
            'v0.8.0', 'v0.8.1', [
                (
                    'external-dns-sync:v0.8.0',
                    'external-dns-sync:v0.8.1',
                ),
            ],
        ),
        (
            'container-schedule', '2', '3',
            'v0.6.0', 'v0.6.1', [
                (
                    'container-cron:v0.6.0',
                    'container-cron:v0.6.1',
                ),
            ],
        ),
        (
            'ipsec-overlay', '12', '13',
            'v0.3.10', 'v0.3.11', [
                (
                    'ipsec-vxlan-overlay-network:v0.14.38',
                    'ipsec-vxlan-overlay-network:v0.14.40',
                ),
            ],
        ),
        (
            'layer-2-flat-network', '6', '7',
            'v0.3.4', 'v0.3.5', [
                (
                    'ipsec-vxlan-overlay-network:v0.14.37',
                    'ipsec-vxlan-overlay-network:v0.14.40',
                ),
            ],
        ),
        (
            'per-host-subnet-network', '4', '5',
            'v0.3.2', 'v0.3.3', [
                (
                    'ipsec-vxlan-overlay-network:v0.14.34',
                    'ipsec-vxlan-overlay-network:v0.14.40',
                ),
            ],
        ),
        (
            'vxlan-overlay-network', '5', '6',
            'v0.3.3', 'v0.3.4', [
                (
                    'ipsec-vxlan-overlay-network:v0.14.34',
                    'ipsec-vxlan-overlay-network:v0.14.40',
                ),
            ],
        ),
        (
            'nfs-storage', '2', '3',
            'v0.10.0', 'v0.11.1', [
                (
                    'nfs-storage-driver:v0.10.0',
                    'nfs-storage-driver:v0.11.1',
                ),
            ],
        ),
        (
            'amazon-ebs-storage', '2', '3',
            'v0.10.0', 'v0.11.1', [
                (
                    'ebs-storage-driver:v0.10.0',
                    'ebs-storage-driver:v0.11.1',
                ),
            ],
        ),
        (
            'amazon-efs-storage', '2', '3',
            'v0.10.0', 'v0.11.1', [
                (
                    'efs-storage-driver:v0.10.0',
                    'efs-storage-driver:v0.11.1',
                ),
            ],
        ),
        (
            'resource-scheduler', '5', '6',
            'v0.8.19', 'v0.8.20', [
                (
                    'resource-scheduler:v0.8.19',
                    'resource-scheduler:v0.8.20',
                ),
            ],
        ),
        (
            'ecr-credential-sync', '3', '4',
            'v3.1.5', 'v3.1.6', [
                (
                    'ecr-credential-sync:v3.1.5',
                    'ecr-credential-sync:v3.1.6',
                ),
            ],
        ),
    ])
def test_october_security_revisions_preserve_contract(
        template, old_number, new_number, old_version, new_version,
        replacements):
    prefix = 'infra-templates/' + template + '/'
    for filename in ('docker-compose.yml', 'docker-compose.yml.tpl'):
        old_path = _file(prefix + old_number + '/' + filename)
        if not os.path.isfile(old_path):
            continue
        with open(old_path, encoding='utf-8') as source:
            expected = source.read()
        for old_image, new_image in replacements:
            expected = expected.replace(old_image, new_image)
        with open(_file(prefix + new_number + '/' + filename),
                  encoding='utf-8') as source:
            assert source.read() == expected
    for filename in ('rancher-compose.yml',):
        with open(_file(prefix + old_number + '/' + filename),
                  encoding='utf-8') as source:
            expected = source.read()
        if filename == 'rancher-compose.yml':
            expected = expected.replace(
                '  version: ' + old_version + '\n',
                '  version: ' + new_version + '\n')
        with open(_file(prefix + new_number + '/' + filename),
                  encoding='utf-8') as source:
            assert source.read() == expected
    # Documentation follows the new published inputs; runtime definitions above
    # remain byte-identical apart from the reviewed image/version replacements.
    for filename in ('README.md', 'README.zh-TW.md'):
        with open(_file(prefix + old_number + '/' + filename),
                  encoding='utf-8') as source:
            old_doc = source.read()
        with open(_file(prefix + new_number + '/' + filename),
                  encoding='utf-8') as source:
            new_doc = source.read()
        assert new_doc.strip()
        for old_image, new_image in replacements:
            if old_image in old_doc:
                assert new_image in new_doc
                assert old_image not in new_doc
    for number in (old_number, new_number):
        retained = _get_json(_catalog_url(
            '/v1-catalog/templateversions/{}:infra*{}:{}'.format(
                _catalog_name(), template, number)))
        assert 'rancher-compose.yml' in retained['files']


def test_catalog_commit_is_pinned():
    catalogs = _get_json(_catalog_url('/v1-catalog/catalogs'))
    data = catalogs.get('data', [])
    assert len(data) == 1
    assert data[0]['branch'] == _current_branch()
    assert data[0]['pinnedCommit'] == _catalog_commit()


def test_network_services13_preserves_contract_and_published_identities():
    template = 'infra-templates/network-services'
    old_image = 'ghcr.io/pasturestack/network-plugin-manager:v0.8.24'
    image = 'ghcr.io/pasturestack/network-plugin-manager:v0.8.25'
    with open(_file(template + '/12/docker-compose.yml.tpl'),
              encoding='utf-8') as source:
        old_compose = source.read()
    with open(_file(template + '/13/docker-compose.yml.tpl'),
              encoding='utf-8') as source:
        compose = source.read()
    assert old_compose.count('image: ' + old_image) == 1
    assert compose == old_compose.replace(old_image, image).replace(
        'metadata-service:v0.10.5', 'metadata-service:v0.10.6')
    with open(_file(template + '/12/rancher-compose.yml'),
              encoding='utf-8') as source:
        old_catalog = source.read()
    with open(_file(template + '/13/rancher-compose.yml'),
              encoding='utf-8') as source:
        catalog = source.read()
    assert catalog == old_catalog.replace(
        '  version: v0.3.10\n', '  version: v0.3.11\n')
    with open(_file('catalog-images.json'), encoding='utf-8') as source:
        images = {
            item['reference']: item for item in json.load(source)['images']
        }
    assert images[old_image]['sourceCommit'] == (
        'f34bbca219ddd84b94f4b3f833e04d67b9c8ce03')
    assert images[image]['sourceCommit'] == (
        '461182e1fcd09527509359f5c551704303689c04')
    assert images[image]['manifestDigest'] == (
        'sha256:9a66894138dc6dded756c5e4b80e6d23'
        '5698d911031641f6c45763ad9b32d94e')
    assert images[image]['sbom']['sha256'] == (
        '91f7cce56e1755e9625e2c6bfd0c6f0c'
        '9f73d9158b887037520abca7930186b2')
    scan = images[image]['vulnerabilityScan']
    assert all(scan[level] == 0 for level in (
        'high', 'critical', 'low', 'medium', 'unknown', 'secrets'))
    publication = images[image]['publicationVerification']
    assert publication['sourceCommit'] == images[image]['sourceCommit']
    assert publication['workflowRun'] == (
        'https://github.com/PastureStack/network-plugin-manager/actions/runs/'
        '40013313015')
    assert publication['anonymousReadback'] is True
    assert publication['githubReleaseImmutable'] is False
    assert publication['provenancePredicateType'] == (
        'https://slsa.dev/provenance/v1')
    metadata = images['ghcr.io/pasturestack/metadata-service:v0.10.6']
    assert metadata['sourceCommit'] == (
        '3db2e1cd53530a04282f5c2448426334ea4d92a8')
    assert metadata['manifestDigest'] == (
        'sha256:88267d800365d354f06519014a3e4f7ce'
        '967d05d4805e5a705944980e30449ff')
    assert metadata['sbom']['sha256'] == (
        '35fd5be38787438350e0eeea87eaf2eab'
        '6e64575fef895103c44570523e5db4a')
    scan = metadata['vulnerabilityScan']
    assert scan['rawFindings'] == scan['reviewedUnfixedOccurrences'] == 44
    assert (scan['medium'], scan['low']) == (38, 6)
    assert all(scan[level] == 0 for level in (
        'high', 'critical', 'unknown', 'secrets', 'fixedAvailable'))
    publication = metadata['publicationVerification']
    assert publication['githubReleaseImmutable'] is False
    assert publication['workflowRun'] == (
        'https://github.com/PastureStack/metadata-service/actions/runs/'
        '40016315561')


def test_ipsec38_template_preserves_version11_contract():
    template = 'infra-templates/ipsec-overlay'
    old_image = 'ghcr.io/pasturestack/ipsec-vxlan-overlay-network:v0.14.35'
    image = 'ghcr.io/pasturestack/ipsec-vxlan-overlay-network:v0.14.38'
    with open(_file(template + '/11/docker-compose.yml.tpl'),
              encoding='utf-8') as source:
        old_compose = source.read()
    with open(_file(template + '/12/docker-compose.yml.tpl'),
              encoding='utf-8') as source:
        compose = source.read()
    assert old_compose.count('image: ' + old_image) == 4
    assert compose == old_compose.replace(old_image, image)
    assert '@sha256:' not in compose
    with open(_file(template + '/11/rancher-compose.yml'),
              encoding='utf-8') as source:
        old_catalog = source.read()
    with open(_file(template + '/12/rancher-compose.yml'),
              encoding='utf-8') as source:
        catalog = source.read()
    assert catalog == old_catalog.replace(
        '  version: v0.3.9\n', '  version: v0.3.10\n')

    with open(_file('catalog-images.json'), encoding='utf-8') as source:
        images = {
            item['reference']: item for item in json.load(source)['images']
        }
    assert images[old_image]['sourceCommit'] == (
        'bf81eef04ae64fd94155595fde8be7581900f4a8')
    assert images[old_image]['manifestDigest'] == (
        'sha256:452405892045346614eac8e2680b1b715'
        'bf6df3913ea4435dbee3550b60c07bb')
    assert images[image]['sourceCommit'] == (
        'c143e9a5f21ba6df2d1c5002340c71777f875c89')
    assert images[image]['manifestDigest'] == (
        'sha256:5b29e08dca8a92fc0ecc7f9d0fdae045'
        '7b89daa9d02b1c1c3257bc9dd617c3ae')
    assert images[image]['platforms'] == ['linux/amd64']
    scan = images[image]['vulnerabilityScan']
    assert scan['scope'] == 'published runtime image'
    assert scan['high'] == scan['critical'] == scan['secrets'] == 0


def test_npm22_template_preserves_version9_contract():
    template = 'infra-templates/network-services'
    old_image = 'ghcr.io/pasturestack/network-plugin-manager:v0.8.21'
    image = 'ghcr.io/pasturestack/network-plugin-manager:v0.8.22'
    with open(_file(template + '/9/docker-compose.yml.tpl'),
              encoding='utf-8') as source:
        old_compose = source.read()
    with open(_file(template + '/10/docker-compose.yml.tpl'),
              encoding='utf-8') as source:
        compose = source.read()
    assert old_compose.count('image: ' + old_image) == 1
    assert compose == old_compose.replace(old_image, image)
    assert '@sha256:' not in compose
    with open(_file(template + '/9/rancher-compose.yml'),
              encoding='utf-8') as source:
        old_catalog = source.read()
    with open(_file(template + '/10/rancher-compose.yml'),
              encoding='utf-8') as source:
        catalog = source.read()
    assert catalog == old_catalog.replace(
        '  version: v0.3.7\n', '  version: v0.3.8\n')

    with open(_file('catalog-images.json'), encoding='utf-8') as source:
        images = {
            item['reference']: item for item in json.load(source)['images']
        }
    assert images[old_image]['sourceCommit'] == (
        '2f2418423022264695f90960f4a80b9d20c5826f')
    assert images[old_image]['manifestDigest'] == (
        'sha256:aab4c05b0801feeca40fa9cb82a52fbfb'
        'fe506c609d3df2024fbc07ef4b968e9')
    assert images[image]['sourceCommit'] == (
        '7b0920aa0c8f3b2c009c9c47c94c4d21b77c7077')
    assert images[image]['manifestDigest'] == (
        'sha256:63eebc25b5795bd0dce56630841b4d33'
        'b4aa657f446c63ae8978c37357bb030a')
    assert images[image]['platforms'] == ['linux/amd64']
    scan = images[image]['vulnerabilityScan']
    assert scan['scope'] == 'published runtime image'
    assert scan['high'] == scan['critical'] == scan['secrets'] == 0
    assert scan['databaseDownloadedAt'] == '2026-10-07T02:47:02Z'


@pytest.mark.parametrize('number,label,image_tag', [
    ('9', 'v0.3.7', 'v0.8.21'),
    ('10', 'v0.3.8', 'v0.8.22'),
])
def test_network_services_upgrade_versions_remain_available(
        number, label, image_tag):
    version = _get_json(_catalog_url(
        '/v1-catalog/templateversions/{}:infra*network-services:{}'.format(
            _catalog_name(), number)))
    files = version['files']
    assert ('image: ghcr.io/pasturestack/network-plugin-manager:' + image_tag
            in files['docker-compose.yml.tpl'])
    assert '  version: ' + label + '\n' in files['rancher-compose.yml']
    assert 'README.md' in files
    assert 'README.zh-TW.md' in files


def test_scheduler19_template_preserves_version4_contract():
    template = 'infra-templates/resource-scheduler'
    old_image = 'ghcr.io/pasturestack/resource-scheduler:v0.8.18'
    image = 'ghcr.io/pasturestack/resource-scheduler:v0.8.19'
    with open(_file(template + '/4/docker-compose.yml'),
              encoding='utf-8') as source:
        old_compose = source.read()
    with open(_file(template + '/5/docker-compose.yml'),
              encoding='utf-8') as source:
        compose = source.read()
    assert old_compose.count('image: ' + old_image) == 1
    assert compose == old_compose.replace(old_image, image)
    assert '@sha256:' not in compose
    with open(_file(template + '/4/rancher-compose.yml'),
              encoding='utf-8') as source:
        old_catalog = source.read()
    with open(_file(template + '/5/rancher-compose.yml'),
              encoding='utf-8') as source:
        catalog = source.read()
    assert catalog == old_catalog.replace(
        '  version: v0.8.18\n', '  version: v0.8.19\n')

    with open(_file('catalog-images.json'), encoding='utf-8') as source:
        images = {
            item['reference']: item for item in json.load(source)['images']
        }
    assert images[old_image]['sourceCommit'] == (
        '033f0f4fb9b13b7524216accd5d9bab804a3b69b')
    release = images[image]
    assert release['sourceCommit'] == (
        'd1720ddb65a285ed615f1461ccb44e50c2ad67a7')
    assert release['platforms'] == ['linux/amd64']
    assert release['manifestDigest'] == (
        'sha256:46dfecc72fc1fceab5c66f881f464498'
        '74b6a084a208f59c6ef1184a0d15c3f9')
    scan = release['vulnerabilityScan']
    assert scan['scope'] == 'published runtime image'
    assert scan['high'] == scan['critical'] == scan['secrets'] == 0
    assert scan['fixedAvailable'] == scan['actionable'] == 0
    assert scan['low'] + scan['medium'] == scan['vendorUnfixedLowMedium']
    assert scan['disposition'] == 'under_investigation'
    sbom = release['sbom']
    assert sbom['format'] == 'CycloneDX'
    assert sbom['sha256'] == (
        '1ffbad2e58a5eaa5b7d72c83f8d8586f9'
        'f0eda337aacc41eb8d05a106951dc6e')
    assert sbom['url'].endswith(
        '/v0.8.19/resource-scheduler-0.8.19-image.cdx.json')
    provenance = sbom['provenance']
    assert provenance['verified'] is True
    assert provenance['sourceCommit'] == release['sourceCommit']
    assert provenance['sourceRef'] == 'refs/tags/v0.8.19'
    assert provenance['predicateType'] == 'https://slsa.dev/provenance/v1'
    assert provenance['signerWorkflow'] == (
        'PastureStack/resource-scheduler/.github/workflows/release.yml')
    with open(_file('catalog-provenance.json'), encoding='utf-8') as source:
        maintained = json.load(source)['entries'][
            'resource-scheduler']['retainedReleases']['v0.8.19']
    assert maintained['reference'] == image
    assert maintained['sourceCommit'] == release['sourceCommit']
    assert maintained['manifestDigest'] == release['manifestDigest']
    assert maintained['sbom'] == sbom


@pytest.mark.parametrize('tag,source_commit,manifest_digest,sbom_sha', [
    ('v0.8.20',
     '35d3a67c62df4b22d7167da3d73dd9dbc4905e66',
     'sha256:e5a389273344585fca5c4513060e5289b'
     '30ca13046d8ec286b8563952f1325d4',
     '56de083886f393483d988c210d307d71a0b'
     '9252b5d25a36095b2161bbab15e91'),
    ('v0.8.21',
     'b9f0c18d2318a5ccd6c6d0a2ace27715bec6e8a6',
     'sha256:0818b05b49d73bb789b83932a91df3bf6'
     'a09d78fab3b370a7afe51f5c2ec2bdf',
     '18f6caa7d3400b93808bfdfe8dd6a2107'
     'ae7752a1d1bd6c08c88eea518fcb032'),
])
def test_scheduler_published_provenance_matches_current_and_retained_image(
        tag, source_commit, manifest_digest, sbom_sha):
    image = 'ghcr.io/pasturestack/resource-scheduler:' + tag
    with open(_file('catalog-images.json'), encoding='utf-8') as source:
        release = next(item for item in json.load(source)['images']
                       if item['reference'] == image)
    with open(_file('catalog-provenance.json'), encoding='utf-8') as source:
        entry = json.load(source)['entries']['resource-scheduler']
        maintained = (entry['maintainedRelease'] if tag == 'v0.8.21'
                      else entry['retainedReleases'][tag])
    assert maintained['reference'] == image
    assert maintained['sourceCommit'] == release['sourceCommit'] == source_commit
    assert maintained['manifestDigest'] == release['manifestDigest'] == (
        manifest_digest)
    assert maintained['sbom'] == release['sbom']
    assert release['sbom']['sha256'] == sbom_sha
    assert release['sbom']['provenance']['sourceRef'] == 'refs/tags/' + tag
    assert release['vulnerabilityScan']['fixedAvailable'] == 0


@pytest.mark.parametrize('number,image_tag', [
    ('4', 'v0.8.18'),
    ('5', 'v0.8.19'),
    ('6', 'v0.8.20'),
])
def test_scheduler_upgrade_versions_remain_available(number, image_tag):
    version = _get_json(_catalog_url(
        '/v1-catalog/templateversions/{}:infra*resource-scheduler:{}'.format(
            _catalog_name(), number)))
    files = version['files']
    assert ('image: ghcr.io/pasturestack/resource-scheduler:' + image_tag
            in files['docker-compose.yml'])
    assert '  version: ' + image_tag + '\n' in files['rancher-compose.yml']
    assert 'request_line: GET /healthcheck HTTP/1.0' in (
        files['rancher-compose.yml'])
    assert 'README.md' in files
    assert 'README.zh-TW.md' in files


@pytest.mark.parametrize(
    "template,old_number,new_number,old_version,new_version,replacements",
    [('container-schedule',
      '3',
      '4',
      'v0.6.1',
      'v0.6.2',
      [('container-cron:v0.6.1', 'container-cron:v0.6.2')]),
     ('healthcheck',
      '2',
      '3',
      'v0.3.17',
      'v0.3.18',
      [('metadata-healthcheck:v0.3.17', 'metadata-healthcheck:v0.3.18')]),
     ('ipsec-overlay',
      '13',
      '14',
      'v0.3.11',
      'v0.3.12',
      [('ipsec-vxlan-overlay-network:v0.14.40',
        'ipsec-vxlan-overlay-network:v0.14.41')]),
     ('layer-2-flat-network',
      '7',
      '8',
      'v0.3.5',
      'v0.3.6',
      [('ipsec-vxlan-overlay-network:v0.14.40',
        'ipsec-vxlan-overlay-network:v0.14.41')]),
     ('network-policy-manager',
      '4',
      '5',
      'v0.3.4',
      'v0.3.5',
      [('network-policy-manager:v0.3.2',
        'network-policy-manager:v0.3.3')]),
     ('network-services',
      '13',
      '14',
      'v0.3.11',
      'v0.3.12',
      [('metadata-service:v0.10.6', 'metadata-service:v0.10.7'),
       ('internal-dns:v0.17.13', 'internal-dns:v0.17.14')]),
     ('per-host-subnet-network',
      '5',
      '6',
      'v0.3.3',
      'v0.3.4',
      [('ipsec-vxlan-overlay-network:v0.14.40',
        'ipsec-vxlan-overlay-network:v0.14.41')]),
     ('resource-scheduler',
      '6',
      '7',
      'v0.8.20',
      'v0.8.21',
      [('resource-scheduler:v0.8.20', 'resource-scheduler:v0.8.21')]),
     ('secret-volume-driver',
      '3',
      '4',
      'v0.1.3',
      'v0.1.4',
      [('secrets-flexvolume-plugin:v0.2.1',
        'secrets-flexvolume-plugin:v0.2.2')]),
     ('system-image-preloader',
      '3',
      '4',
      'v0.3.2',
      'v0.3.3',
      [('system-image-preloader:v0.3.2',
        'system-image-preloader:v0.3.3')]),
     ('vault-volume-driver',
      '4',
      '5',
      'v0.2.2',
      'v0.2.3',
      [('vault-secrets-bridge:v0.1.2', 'vault-secrets-bridge:v0.1.3'),
       ('secrets-flexvolume-plugin:v0.2.1',
        'secrets-flexvolume-plugin:v0.2.2')]),
     ('vxlan-overlay-network',
      '6',
      '7',
      'v0.3.4',
      'v0.3.5',
      [('ipsec-vxlan-overlay-network:v0.14.40',
        'ipsec-vxlan-overlay-network:v0.14.41')]),
     ('windows-container-networking',
      '3',
      '4',
      'v0.1.1',
      'v0.1.2',
      [('pod-pause-image:v3.0.5', 'pod-pause-image:v3.0.6')])]
)
def test_qualified_backport_source_contract(
        template, old_number, new_number, old_version, new_version,
        replacements):
    """Only image/version changes; no Catalog Service or runtime required."""
    prefix = "infra-templates/" + template + "/"
    for filename in ("docker-compose.yml", "docker-compose.yml.tpl"):
        old_path = _file(prefix + old_number + "/" + filename)
        if not os.path.isfile(old_path):
            continue
        with open(old_path, encoding="utf-8") as source:
            expected = source.read()
        for old_image, new_image in replacements:
            expected = expected.replace(old_image, new_image)
        with open(_file(prefix + new_number + "/" + filename),
                  encoding="utf-8") as source:
            assert source.read() == expected
    with open(_file(prefix + old_number + "/rancher-compose.yml"),
              encoding="utf-8") as source:
        expected = source.read().replace(
            "  version: " + old_version + "\n",
            "  version: " + new_version + "\n")
    with open(_file(prefix + new_number + "/rancher-compose.yml"),
              encoding="utf-8") as source:
        assert source.read() == expected
    with open(_file(prefix + "config.yml"), encoding="utf-8") as source:
        assert "\nversion: " + new_version + "\n" in source.read()
    for filename in ("README.md", "README.zh-TW.md"):
        with open(_file(prefix + new_number + "/" + filename),
                  encoding="utf-8") as source:
            doc = source.read()
        assert doc.strip()
        for old_image, new_image in replacements:
            assert old_image in doc and new_image in doc
