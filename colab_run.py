# Google Colab / Ngrok Streamlit Runner for EcoWatt
# Run this script in Google Colab to deploy EcoWatt with ngrok tunnel.

import os
import subprocess
import socket
import time
import psutil
from pyngrok import ngrok

def _get_secret(name):
    try:
        from google.colab import userdata
        val = userdata.get(name)
        if val:
            return val
    except Exception:
        pass
    return os.environ.get(name, "")

OPENWEATHER_API_KEY_VALUE = _get_secret("OPENWEATHER_API_KEY") or "40d15d9b8860af245b44d15ee812f496"
NGROK_AUTHTOKEN_VALUE = _get_secret("NGROK_AUTHTOKEN") or "3FXkJDsAj9osZANxjN0KtlK0Qkc_3PSiqjKHNzPu3idjY39Pb"
os.environ["OPENWEATHER_API_KEY"] = OPENWEATHER_API_KEY_VALUE

def find_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        return s.getsockname()[1]

def kill_process_on_port(port):
    for proc in psutil.process_iter(['pid', 'name', 'connections']):
        try:
            for conn in proc.connections(kind='inet'):
                if conn.laddr.port == port and (conn.laddr.ip in ('127.0.0.1', '::1', '0.0.0.0')):
                    print(f"Killing process {proc.pid} ({proc.name()}) on port {port}")
                    proc.terminate()
                    proc.wait(timeout=10)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

# Cleanup existing streamlit processes
for proc in psutil.process_iter(['pid', 'name']):
    if 'streamlit' in proc.info['name'].lower():
        try:
            proc.terminate()
            proc.wait(timeout=10)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

print("Cleaning ngrok processes and disconnecting tunnels...")
ngrok.kill()
try:
    ngrok.disconnect()
except Exception:
    pass

ngrok_config_path = os.path.expanduser("~/.ngrok2/ngrok.yml")
if os.path.exists(ngrok_config_path):
    try:
        os.remove(ngrok_config_path)
    except Exception:
        pass

if NGROK_AUTHTOKEN_VALUE:
    ngrok.set_auth_token(NGROK_AUTHTOKEN_VALUE)

streamlit_port = find_free_port()
print(f"Selected Streamlit port: {streamlit_port}")
kill_process_on_port(streamlit_port)

streamlit_process_cmd = [
    "python",
    "-m", "streamlit",
    "run",
    "app.py",
    "--server.port", str(streamlit_port),
    "--server.address", "127.0.0.1",
    "--server.enableCORS", "false",
    "--server.enableXsrfProtection", "false"
]

# Use os.setsid on Unix (Colab/Linux); on Windows preexec_fn is not supported
preexec = os.setsid if hasattr(os, "setsid") else None
process = subprocess.Popen(
    streamlit_process_cmd,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
    preexec_fn=preexec
)

print(f"Streamlit app is starting on port {streamlit_port} at 127.0.0.1...")
time.sleep(8)

public_url = None
max_retries = 5
for i in range(max_retries):
    try:
        print(f"Attempt {i+1}/{max_retries} to connect ngrok on 127.0.0.1:{streamlit_port}...")
        public_url = ngrok.connect(addr=f"127.0.0.1:{streamlit_port}", proto="http", host_header="127.0.0.1")
        break
    except Exception as e:
        print(f"Ngrok connection failed on attempt {i+1}: {e}")
        if i < max_retries - 1:
            print("Retrying in 8 seconds...")
            ngrok.kill()
            try:
                ngrok.disconnect()
            except Exception:
                pass
            time.sleep(8)

if public_url:
    print(f"\n==========================================")
    print(f"⚡ EcoWatt Streamlit App URL: {public_url}")
    print(f"==========================================\n")
else:
    print("Local Streamlit running at http://127.0.0.1:" + str(streamlit_port))
