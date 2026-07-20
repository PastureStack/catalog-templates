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
    assert len(data) == 4
    by_folder = {item['folderName']: item for item in data}
    assert set(by_folder) == {
        'healthcheck',
        'ipsec-overlay',
        'network-services',
        'web-service',
    }
    assert by_folder['web-service']['name'] == 'Web Service'
    assert by_folder['web-service']['defaultVersion'] == '1.30.4'
    assert by_folder['healthcheck']['name'] == 'Metadata Healthcheck'
    assert by_folder['healthcheck']['defaultVersion'] == 'v0.3.14'
    assert by_folder['ipsec-overlay']['name'] == (
        'PastureStack IPsec Overlay')
    assert by_folder['ipsec-overlay']['defaultVersion'] == '0.3.0-rc1'
    assert by_folder['network-services']['name'] == (
        'PastureStack Network Services')
    assert by_folder['network-services']['defaultVersion'] == '0.3.0-rc2'
    assert by_folder['network-services']['links']['defaultVersion'].endswith(
        ':1')


def test_catalog_compose_shapes_are_runtime_compatible():
    templates = _get_json('http://localhost:8088/v1-catalog/templates')
    by_folder = {
        item['folderName']: item for item in templates.get('data', [])
    }

    web_version = _get_json(
        by_folder['web-service']['links']['defaultVersion'])
    web_files = web_version['files']
    web_docker = web_files['docker-compose.yml']
    web_platform = web_files['rancher-compose.yml']
    assert "version: '2'\nservices:\n  web:" in web_docker
    assert '\nservices:\n' not in web_platform
    assert '\nweb:\n  scale: 1' in web_platform

    health_version = _get_json(
        by_folder['healthcheck']['links']['defaultVersion'])
    health_files = health_version['files']
    health_docker = health_files['docker-compose.yml']
    health_platform = health_files['rancher-compose.yml']
    assert "version: '2'\nservices:\n  healthcheck:" in health_docker
    assert '\nservices:\n' not in health_platform
    assert '\nhealthcheck:\n  scale: 1' in health_platform

    overlay_version = _get_json(
        by_folder['ipsec-overlay']['links']['defaultVersion'])
    overlay_files = overlay_version['files']
    overlay_docker = overlay_files['docker-compose.yml.tpl']
    overlay_platform = overlay_files['rancher-compose.yml']
    overlay_image = (
        'ghcr.io/pasturestack/ipsec-vxlan-overlay-network:v0.14.25@'
        'sha256:f0a7e61a3c35f5f5ba347a0c74d87b736229dcb73a17de90'
        'aaa38df4d94e2e5f'
    )
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
        by_folder['network-services']['links']['defaultVersion'])
    network_files = network_version['files']
    network_docker = network_files['docker-compose.yml.tpl']
    network_platform = network_files['rancher-compose.yml']
    network_manager_image = (
        'ghcr.io/pasturestack/network-plugin-manager:v0.6.34@'
        'sha256:6a1b0f04c5ea2f8e9aac5b26b3ff950847c6fc9ca3786450072a'
        '9ca179e9e67f'
    )
    metadata_image = (
        'ghcr.io/pasturestack/metadata-service:v0.9.11@'
        'sha256:00f35785580edc498f202e1d9670fecf913b5cc15f6d268912'
        'c57662a8b10723'
    )
    dns_image = (
        'ghcr.io/pasturestack/internal-dns:v0.17.11@'
        'sha256:a67a68e5d370ea01d6f1b81ab7340c0ecc6acfad4ed3efdf298d'
        '038c04a00f36'
    )
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


def test_catalog_commit_is_pinned():
    catalogs = _get_json('http://localhost:8088/v1-catalog/catalogs')
    data = catalogs.get('data', [])
    assert len(data) == 1
    assert data[0]['branch'] == _current_branch()
    assert data[0]['pinnedCommit'] == _catalog_commit()
