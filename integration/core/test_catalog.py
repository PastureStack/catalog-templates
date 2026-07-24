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
    assert len(data) == 5
    by_folder = {
        (item.get('templateBase') or 'template', item['folderName']): item
        for item in data
    }
    assert set(by_folder) == {
        ('infra', 'healthcheck'),
        ('infra', 'ipsec-overlay'),
        ('infra', 'network-services'),
        ('infra', 'resource-scheduler'),
        ('project', 'native'),
    }
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
    assert by_folder[('infra', 'network-services')]['name'] == (
        'PastureStack Network Services')
    assert by_folder[('infra', 'network-services')][
        'defaultVersion'] == '0.3.0-rc2'
    assert by_folder[('infra', 'network-services')][
        'links']['defaultVersion'].endswith(
        ':1')
    assert by_folder[('infra', 'resource-scheduler')][
        'name'] == 'Resource Scheduler'
    assert by_folder[('infra', 'resource-scheduler')][
        'defaultVersion'] == 'v0.8.15'
    assert by_folder[('infra', 'resource-scheduler')][
        'links']['defaultVersion'].endswith(
        ':1')
    assert by_folder[('project', 'native')][
        'name'] == 'PastureStack Native'
    assert by_folder[('project', 'native')][
        'defaultVersion'] == '0.3.0-rc6'
    localized = {
        ('infra', 'healthcheck'): (
            '中繼資料健康檢查',
            '依據中繼資料定義檢查工作負載健康狀態，並透過相容控制 API 回報結果。'),
        ('infra', 'ipsec-overlay'): (
            'PastureStack IPsec 加密網路',
            '為受管工作負載提供跨主機的加密網路。'),
        ('infra', 'network-services'): (
            'PastureStack 網路服務',
            '安裝受管工作負載所需的主機網路、中繼資料與內部 DNS 服務。'),
        ('infra', 'resource-scheduler'): (
            '資源排程器',
            '依控制平面事件與目前的中繼資料狀態，排程原生工作負載。'),
        ('project', 'native'): (
            'PastureStack 原生專案範本',
            'PastureStack 原生編排執行環境的預設專案範本。'),
    }
    for key, (name, description) in localized.items():
        labels = by_folder[key]['labels']
        assert labels['io.pasturestack.catalog.name.zh-tw'] == name
        assert labels['io.pasturestack.catalog.description.zh-tw'] == description


def test_catalog_compose_shapes_are_runtime_compatible():
    templates = _get_json('http://localhost:8088/v1-catalog/templates')
    by_folder = {
        (item.get('templateBase') or 'template', item['folderName']): item
        for item in templates.get('data', [])
    }

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
