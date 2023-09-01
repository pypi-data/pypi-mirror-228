import socket
import time
import subprocess
import pkg_resources

class PetronasCommonUtilsService:

    def __init__(self, port=25333):
        # Execute java package and handle connection
        jar_path = pkg_resources.resource_filename('petronas_common_utils', 'resources/petronas-common-utils-1.0-all.jar')
        # Java service connection to port
        self.port = port
        # Execute java model
        command = ["java", "-jar", jar_path]
        self.process = subprocess.Popen(command)
        # Wait an check for port binding from java side
        self.wait_for_port(timeout=10)

    def wait_for_port(self, host='localhost', timeout=60.0):
        """Wait until a port starts accepting TCP connections."""
        start_time = time.time()
        while True:
            try:
                with socket.create_connection((host, self.port), timeout=timeout):
                    break
            except OSError as ex:
                time.sleep(0.01)
                if time.time() - start_time >= timeout:
                    raise TimeoutError(f"Waited too long for the port {self.port} on host {host} to start accepting connections.") from ex
                
    def set_gateway(self, gateway):
        self.gateway = gateway

    def stop(self):
        self.gateway.shutdown()
        if self.process:
            self.process.terminate()
            self.process = None

    def __del__(self):
        self.stop()