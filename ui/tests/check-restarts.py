"""Run with python3 ui/tests/check-restarts.py; requires Docker. No model inference."""
import json
import http.client
from pathlib import Path
import subprocess
import tempfile
import time
import urllib.error
import urllib.request
import uuid


def docker(*args):
    return subprocess.check_output(['docker', *args], text=True).strip()


name = 'ollama-ui-check-' + uuid.uuid4().hex[:8]
containers = []
ui_dir = Path(__file__).resolve().parents[1]
image = name + ':test'
network_created = False
try:
    docker('build', '-q', '-t', image, str(ui_dir))
    docker('network', 'create', name)
    network_created = True
    # Make Docker's allocated subnet explicit so the old IP can be held during the test.
    subnet = json.loads(docker('network', 'inspect', name))[0]['IPAM']['Config'][0]['Subnet']
    docker('network', 'rm', name)
    docker('network', 'create', '--subnet', subnet, name)
    ui = name + '-ui'
    containers.append(ui)
    docker('run', '-d', '--name', ui, '--network', name, '-p', '127.0.0.1::80', image)
    port = docker('port', ui, '80/tcp').rsplit(':', 1)[1]
    origin = 'http://127.0.0.1:' + port

    def wait_for(path, expected=None):
        deadline = time.monotonic() + 20
        while time.monotonic() < deadline:
            try:
                with urllib.request.urlopen(origin + path, timeout=2) as response:
                    body = response.read().decode()
                    if expected is None or expected in body:
                        return body
            except (urllib.error.URLError, http.client.HTTPException, OSError):
                pass
            time.sleep(0.25)
        raise AssertionError('UI did not recover at ' + path)

    assert 'Model Manager' in wait_for('/')  # Starts before backend DNS exists.
    try:
        urllib.request.urlopen(origin + '/api/tags', timeout=5)
        raise AssertionError('Missing backend unexpectedly responded')
    except urllib.error.HTTPError as error:
        assert error.code == 502

    with tempfile.TemporaryDirectory(prefix='ollama-ui-check-') as directory:
        config = Path(directory) / 'default.conf'
        config.write_text('''server {
          listen 11434;
          default_type application/json;
          location /api/tags { return 200 '{"models":[],"uri":"$request_uri"}'; }
          location /v1/models { return 200 '{"object":"list","data":[]}'; }
        }''')
        backend = name + '-backend'
        containers.append(backend)

        def start_backend():
            docker('run', '-d', '--name', backend, '--network', name,
                   '--network-alias', 'ollama', '-v',
                   str(config) + ':/etc/nginx/conf.d/default.conf:ro', 'nginx:1.27-alpine')
            return next(iter(json.loads(docker('inspect', backend))[0]
                             ['NetworkSettings']['Networks'].values()))['IPAddress']

        old_ip = start_backend()
        assert json.loads(wait_for('/api/tags?check=1', 'models'))['uri'] == '/api/tags?check=1'
        assert json.loads(wait_for('/v1/models', 'list'))['object'] == 'list'
        started_at = json.loads(docker('inspect', ui))[0]['State']['StartedAt']
        docker('rm', '-f', backend)
        blocker = name + '-old-ip'
        containers.append(blocker)
        docker('run', '-d', '--name', blocker, '--network', name, '--ip', old_ip,
               'nginx:1.27-alpine')
        new_ip = start_backend()
        assert new_ip != old_ip
        assert 'models' in wait_for('/api/tags', 'models')
        assert 'list' in wait_for('/v1/models', 'list')
        assert json.loads(docker('inspect', ui))[0]['State']['StartedAt'] == started_at
    print('PASS: UI starts without backend and recovers after backend IP changes; both API prefixes work.')
finally:
    for container in reversed(containers):
        subprocess.run(['docker', 'rm', '-fv', container], stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL)
    if network_created:
        subprocess.run(['docker', 'network', 'rm', name], stdout=subprocess.DEVNULL)
    subprocess.run(['docker', 'image', 'rm', image], stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL)
