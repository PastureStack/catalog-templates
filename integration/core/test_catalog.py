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


def _kubernetes_version_url(version_id):
    return _catalog_url(
        '/v1-catalog/templateversions/{}:infra*kubernetes-cluster:{}'.format(
            _catalog_name(), version_id))


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
    assert len(data) == 23
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
        ('infra', 'kubernetes-cluster'),
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
        localized_name = template.get('labels', {}).get(
            'io.pasturestack.catalog.name.zh-tw', '')
        assert not localized_name.casefold().startswith('pasturestack ')

    assert by_folder[('infra', 'amazon-ebs-storage')][
        'name'] == 'Amazon EBS Storage'
    assert by_folder[('infra', 'amazon-ebs-storage')][
        'defaultVersion'] == 'v0.10.0-pasturestack.1'
    assert by_folder[('infra', 'amazon-ebs-storage')][
        'links']['defaultVersion'].endswith(
        ':2')
    assert by_folder[('infra', 'amazon-efs-storage')][
        'name'] == 'Amazon EFS Storage'
    assert by_folder[('infra', 'amazon-efs-storage')][
        'defaultVersion'] == 'v0.10.0-pasturestack.1'
    assert by_folder[('infra', 'amazon-efs-storage')][
        'links']['defaultVersion'].endswith(
        ':2')
    assert by_folder[('infra', 'container-schedule')][
        'name'] == 'Container Schedule'
    assert by_folder[('infra', 'container-schedule')][
        'defaultVersion'] == 'v0.6.0-pasturestack.1'
    assert by_folder[('infra', 'container-schedule')][
        'links']['defaultVersion'].endswith(
        ':2')
    assert by_folder[('infra', 'ecr-credential-sync')][
        'name'] == 'Amazon ECR Credential Sync'
    assert by_folder[('infra', 'ecr-credential-sync')][
        'defaultVersion'] == 'v3.1.0-pasturestack.1'
    assert by_folder[('infra', 'ecr-credential-sync')][
        'links']['defaultVersion'].endswith(
        ':2')
    assert by_folder[('infra', 'healthcheck')][
        'name'] == 'Metadata Healthcheck'
    assert by_folder[('infra', 'healthcheck')][
        'defaultVersion'] == 'v0.3.16-pasturestack.1'
    assert by_folder[('infra', 'healthcheck')][
        'links']['defaultVersion'].endswith(
        ':1')
    assert by_folder[('infra', 'ipsec-overlay')]['name'] == (
        'IPsec Overlay')
    assert by_folder[('infra', 'ipsec-overlay')][
        'defaultVersion'] == '0.3.0-rc2-pasturestack.1'
    assert by_folder[('infra', 'ipsec-overlay')][
        'links']['defaultVersion'].endswith(
        ':2')
    assert by_folder[('infra', 'kubernetes-cluster')]['name'] == (
        'Kubernetes Cluster')
    assert by_folder[('infra', 'kubernetes-cluster')][
        'defaultVersion'] == 'v1.12.10-pasturestack.6'
    assert by_folder[('infra', 'kubernetes-cluster')][
        'links']['defaultVersion'].endswith(
        ':6')
    assert by_folder[('infra', 'layer-2-flat-network')]['name'] == (
        'Layer 2 Flat Network')
    assert by_folder[('infra', 'layer-2-flat-network')][
        'defaultVersion'] == '0.3.0-rc8-pasturestack.1'
    assert by_folder[('infra', 'layer-2-flat-network')][
        'links']['defaultVersion'].endswith(
        ':2')
    assert by_folder[('infra', 'network-diagnostics')]['name'] == (
        'Network Diagnostics')
    assert by_folder[('infra', 'network-diagnostics')][
        'defaultVersion'] == 'v0.2.0-pasturestack.1'
    assert by_folder[('infra', 'network-diagnostics')][
        'links']['defaultVersion'].endswith(
        ':2')
    assert by_folder[('infra', 'network-policy-manager')]['name'] == (
        'Network Policy Manager')
    assert by_folder[('infra', 'network-policy-manager')][
        'defaultVersion'] == 'v0.3.1-pasturestack.1'
    assert by_folder[('infra', 'network-policy-manager')][
        'links']['defaultVersion'].endswith(
        ':2')
    assert by_folder[('infra', 'network-services')]['name'] == (
        'Network Services')
    assert by_folder[('infra', 'network-services')][
        'defaultVersion'] == '0.3.0-rc2-pasturestack.1'
    assert by_folder[('infra', 'network-services')][
        'links']['defaultVersion'].endswith(
        ':2')
    assert by_folder[('infra', 'nfs-storage')][
        'name'] == 'NFS Storage'
    assert by_folder[('infra', 'nfs-storage')][
        'defaultVersion'] == 'v0.10.0-pasturestack.1'
    assert by_folder[('infra', 'nfs-storage')][
        'links']['defaultVersion'].endswith(
        ':2')
    assert by_folder[('infra', 'secret-volume-driver')][
        'name'] == 'Secret Volume'
    assert by_folder[('infra', 'secret-volume-driver')][
        'defaultVersion'] == 'v0.1.1-pasturestack.1'
    assert by_folder[('infra', 'secret-volume-driver')][
        'links']['defaultVersion'].endswith(
        ':2')
    assert by_folder[('infra', 'vault-volume-driver')][
        'name'] == 'Vault Volume'
    assert by_folder[('infra', 'vault-volume-driver')][
        'defaultVersion'] == 'v0.2.1-pasturestack.1'
    assert by_folder[('infra', 'vault-volume-driver')][
        'links']['defaultVersion'].endswith(
        ':3')
    assert by_folder[('infra', 'per-host-subnet-network')]['name'] == (
        'Per-Host Subnet Network')
    assert by_folder[('infra', 'per-host-subnet-network')][
        'defaultVersion'] == '0.3.0-rc8-pasturestack.1'
    assert by_folder[('infra', 'per-host-subnet-network')][
        'links']['defaultVersion'].endswith(
        ':2')
    assert by_folder[('infra', 'resource-scheduler')][
        'name'] == 'Resource Scheduler'
    assert by_folder[('infra', 'resource-scheduler')][
        'defaultVersion'] == 'v0.8.15-pasturestack.1'
    assert by_folder[('infra', 'resource-scheduler')][
        'links']['defaultVersion'].endswith(
        ':2')
    assert by_folder[('infra', 'route53-dns-sync')][
        'name'] == 'Route 53 DNS Sync'
    assert by_folder[('infra', 'route53-dns-sync')][
        'defaultVersion'] == 'v0.8.0-pasturestack.1'
    assert by_folder[('infra', 'route53-dns-sync')][
        'links']['defaultVersion'].endswith(
        ':2')
    assert by_folder[('infra', 'system-image-preloader')]['name'] == (
        'System Image Preloader')
    assert by_folder[('infra', 'system-image-preloader')][
        'defaultVersion'] == 'v0.3.0-pasturestack.1'
    assert by_folder[('infra', 'system-image-preloader')][
        'links']['defaultVersion'].endswith(
        ':2')
    assert by_folder[('infra', 'vxlan-overlay-network')]['name'] == (
        'VXLAN Overlay Network')
    assert by_folder[('infra', 'vxlan-overlay-network')][
        'defaultVersion'] == '0.3.0-rc9-pasturestack.1'
    assert by_folder[('infra', 'vxlan-overlay-network')][
        'links']['defaultVersion'].endswith(
        ':2')
    assert by_folder[('infra', 'windows-container-networking')][
        'name'] == 'Windows Container Networking'
    assert by_folder[('infra', 'windows-container-networking')][
        'defaultVersion'] == 'v0.1.0-windows-ltsc2022-pasturestack.1'
    assert by_folder[('infra', 'windows-container-networking')][
        'links']['defaultVersion'].endswith(
        ':2')
    assert by_folder[('infra', 'windows-ecr-credential-sync')][
        'name'] == 'Windows ECR Credential Sync'
    assert by_folder[('infra', 'windows-ecr-credential-sync')][
        'defaultVersion'] == 'v3.1.2-windows-ltsc2022-pasturestack.1'
    assert by_folder[('infra', 'windows-ecr-credential-sync')][
        'links']['defaultVersion'].endswith(
        ':2')
    assert by_folder[('infra', 'windows-network-services')][
        'name'] == 'Windows Network Services'
    assert by_folder[('infra', 'windows-network-services')][
        'defaultVersion'] == 'v0.3.0-windows-ltsc2022-pasturestack.1'
    assert by_folder[('infra', 'windows-network-services')][
        'links']['defaultVersion'].endswith(
        ':2')
    assert by_folder[('project', 'native')][
        'name'] == 'Native'
    assert by_folder[('project', 'native')][
        'defaultVersion'] == '0.3.0-rc6'
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
        ('infra', 'kubernetes-cluster'): (
            'Kubernetes 叢集',
            '部署維護中的 Kubernetes 1.12 相容控制平面與主機服務。'),
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
    assert len(provenance['entries']) == 22
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
    assert localized_question_count == 171


def test_catalog_compose_shapes_are_runtime_compatible():
    templates = _get_json(_catalog_url('/v1-catalog/templates'))
    by_folder = {
        (item.get('templateBase') or 'template', item['folderName']): item
        for item in templates.get('data', [])
    }

    kubernetes_version = _get_json(
        by_folder[('infra', 'kubernetes-cluster')][
            'links']['defaultVersion'])
    kubernetes_files = kubernetes_version['files']
    kubernetes_docker = kubernetes_files['docker-compose.yml.tpl']
    kubernetes_platform = kubernetes_files['rancher-compose.yml']
    expected_kubernetes_images = {
        'ghcr.io/pasturestack/kubernetes-package:'
        'v1.12.10-pasturestack.4': 6,
        'ghcr.io/pasturestack/etcd-compat:'
        'v2.3.7-pasturestack.2': 1,
        'ghcr.io/pasturestack/kubectl-service:'
        'v0.9.11-pasturestack.7': 2,
        'ghcr.io/pasturestack/hosts-file-updater:'
        'v0.0.4-pasturestack.1': 1,
        'ghcr.io/pasturestack/kubernetes-agent:'
        'v0.7.2-pasturestack.1': 1,
        'ghcr.io/pasturestack/kubernetes-authentication-bridge:'
        'v0.0.11-pasturestack.1': 1,
        'ghcr.io/pasturestack/load-balancer-service:v0.9.25': 1,
        'ghcr.io/pasturestack/kubernetes-data-helper-image:'
        'v0.1.1-pasturestack.1': 1,
    }
    for image, count in expected_kubernetes_images.items():
        assert kubernetes_docker.count(
            'image: {}'.format(image)) == count
    for version_id in ('2', '3', '4'):
        retained = _get_json(_kubernetes_version_url(version_id))
        retained_docker = retained['files']['docker-compose.yml.tpl']
        assert retained_docker.count(
            'image: ghcr.io/pasturestack/etcd-compat:'
            'v2.3.7-pasturestack.1') == 1
        assert 'v2.3.7-pasturestack.2' not in retained_docker
    revision_five = _get_json(_kubernetes_version_url('5'))
    revision_five_docker = revision_five['files']['docker-compose.yml.tpl']
    assert revision_five['version'] == 'v1.12.10-pasturestack.5'
    assert revision_five_docker.count(
        'image: ghcr.io/pasturestack/kubernetes-package:'
        'v1.12.10-pasturestack.3') == 6
    assert revision_five_docker.count(
        'image: ghcr.io/pasturestack/kubectl-service:'
        'v0.9.11-pasturestack.5') == 2
    assert revision_five_docker.count(
        'image: ghcr.io/pasturestack/etcd-compat:'
        'v2.3.7-pasturestack.2') == 1
    assert kubernetes_docker.count(
        '/var/lib/docker:/var/lib/docker:rslave,z') == 2
    assert '/var/lib/docker:/var/lib/docker:z' not in kubernetes_docker
    assert kubernetes_docker.count(
        '/var/lib/kubelet:/var/lib/kubelet:shared,z') == 2
    assert 'ghcr.io/pasturestack/pod-pause-image:' in (
        kubernetes_platform)
    assert '@sha256:' not in kubernetes_docker
    assert '@sha256:' not in kubernetes_platform
    assert 'addon-starter:' not in kubernetes_docker
    assert 'ENABLE_ADDONS' not in kubernetes_platform
    assert 'platform-kubernetes-agent:' in kubernetes_docker
    assert 'platform-kubernetes-authentication:' in kubernetes_docker
    assert 'platform-ingress-controller:' in kubernetes_docker
    assert 'rancher-kubernetes-agent:' not in kubernetes_docker
    assert 'rancher-kubernetes-auth:' not in kubernetes_docker
    assert 'rancher-ingress-controller:' not in kubernetes_docker
    assert 'PASTURESTACK_DEBUG' in kubernetes_docker
    assert 'RANCHER_DEBUG' not in kubernetes_docker

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
    health_image = 'ghcr.io/pasturestack/metadata-healthcheck:v0.3.16'
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

    diagnostics_version = _get_json(
        by_folder[('infra', 'network-diagnostics')][
            'links']['defaultVersion'])
    diagnostics_files = diagnostics_version['files']
    diagnostics_docker = diagnostics_files['docker-compose.yml.tpl']
    diagnostics_platform = diagnostics_files['rancher-compose.yml']
    diagnostics_agent_image = (
        'ghcr.io/pasturestack/network-diagnostics-agent:v0.2.0')
    diagnostics_service_image = (
        'ghcr.io/pasturestack/network-diagnostics-service:v0.2.0')
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
    assert "'${PUBLISHED_PORT}:8080'" in diagnostics_docker
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
        'ghcr.io/pasturestack/network-policy-manager:v0.3.1')
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
    assert 'request_line: GET /readyz HTTP/1.0' in policy_platform
    assert 'port: 8092' in policy_platform
    assert 'strategy: none' in policy_platform

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

    secret_version = _get_json(
        by_folder[('infra', 'secret-volume-driver')][
            'links']['defaultVersion'])
    secret_files = secret_version['files']
    secret_docker = secret_files['docker-compose.yml']
    secret_platform = secret_files['rancher-compose.yml']
    secret_image = (
        'ghcr.io/pasturestack/secrets-flexvolume-plugin:v0.1.1')
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
        'ghcr.io/pasturestack/vault-secrets-bridge:v0.1.1')
    vault_driver_image = (
        'ghcr.io/pasturestack/secrets-flexvolume-plugin:v0.2.0')
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

    windows_ecr_version = _get_json(
        by_folder[('infra', 'windows-ecr-credential-sync')][
            'links']['defaultVersion'])
    windows_ecr_files = windows_ecr_version['files']
    windows_ecr_docker = windows_ecr_files['docker-compose.yml.tpl']
    windows_ecr_platform = windows_ecr_files['rancher-compose.yml']
    windows_ecr_image = (
        'ghcr.io/pasturestack/ecr-credential-sync-windows:'
        'v3.1.2-windows-ltsc2022')
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
        'v0.9.12-windows-ltsc2022')
    windows_dns_image = (
        'ghcr.io/pasturestack/internal-dns-windows:'
        'v0.17.12-windows-ltsc2022')
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
        'v3.0.1-pasturestack.1')
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


def test_catalog_commit_is_pinned():
    catalogs = _get_json(_catalog_url('/v1-catalog/catalogs'))
    data = catalogs.get('data', [])
    assert len(data) == 1
    assert data[0]['branch'] == _current_branch()
    assert data[0]['pinnedCommit'] == _catalog_commit()
