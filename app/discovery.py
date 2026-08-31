import subprocess
import re
import platform


def discover_gateway():

    system = platform.system().lower()

    try:

        if system == "windows":

            result = subprocess.check_output(
                ["ipconfig"],
                text=True,
                encoding="utf-8",
                errors="ignore"
            )

            matches = re.findall(
                r"Default Gateway[ .:]*([\d.]+)",
                result
            )

            for gateway in matches:

                if gateway and gateway != "0.0.0.0":
                    return gateway

        else:

            result = subprocess.check_output(
                ["ip", "route"],
                text=True,
                encoding="utf-8",
                errors="ignore"
            )

            match = re.search(
                r"default via ([\d.]+)",
                result
            )

            if match:
                return match.group(1)

    except Exception:
        pass

    return None