import subprocess
import threading
import time
from mitmproxy import proxy, options
from mitmproxy.tools.dump import DumpMaster

def automate_sqlmap_with_mitmproxy():
    sqlmap_command = ["sqlmap", "-r", "-", "--batch", "--level=5", "--risk=3"]
    mitmproxy_opts = options.Options(listen_host='127.0.0.1', listen_port=8080)
    m = DumpMaster(opts=mitmproxy_opts)
    config = proxy.config.ProxyConfig(mitmproxy_opts)
    m.server = proxy.server.ProxyServer(config)
    # Run mitmproxy in a separate thread
    t = threading.Thread(target=m.run)
    t.start()
    try:
        while True:
            with open('captured_request.txt', 'r') as file:
                request_data = file.read()
                process = subprocess.Popen(sqlmap_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, stderr = process.communicate(input=request_data.encode())
                print("SQLMap output:")
                print(stdout.decode())
                if stderr:
                    print("Error occurred:")
                    print(stderr.decode())
            time.sleep(5)
    except Exception as e:
        print("An error occurred:", e)
    finally:
        m.shutdown()
        t.join()

automate_sqlmap_with_mitmproxy()