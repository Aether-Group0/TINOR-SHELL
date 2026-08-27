import ipaddress
import requests


class Config:
    """Configuration class for color codes and messages."""

    COLORS = {
        "lblue": "\033[96m",
        "red": "\033[91m",
        "grn": "\033[32m",
        "ylw": "\033[93m",
        "reset": "\033[0m",
    }

    @property
    def banner(self):
        """Return the application banner."""
        return f"""
{self.COLORS['lblue']}╔════════════════════════════════════════════════════════╗
{self.COLORS['lblue']}║                                                        ║
{self.COLORS['lblue']}║   {self.COLORS['red']}██╗  ██████╗      {self.COLORS['grn']}IP Location Finder                 {self.COLORS['lblue']}║
{self.COLORS['lblue']}║   {self.COLORS['red']}██║  ██╔══██╗     {self.COLORS['grn']}Secure API Edition                 {self.COLORS['lblue']}║
{self.COLORS['lblue']}║   {self.COLORS['red']}██║  ██████╔╝     {self.COLORS['grn']}Powered by {self.COLORS['ylw']}ipinfo.io             {self.COLORS['lblue']}║
{self.COLORS['lblue']}║   {self.COLORS['red']}██║  ██╔═══╝      {self.COLORS['ylw']}Version {self.COLORS['red']}2.0                    {self.COLORS['lblue']}║
{self.COLORS['lblue']}║   {self.COLORS['red']}██║  ██║                                      {self.COLORS['lblue']}║
{self.COLORS['lblue']}║   {self.COLORS['red']}╚═╝  ╚═╝                                      {self.COLORS['lblue']}║
{self.COLORS['lblue']}║                                                        ║
{self.COLORS['lblue']}╚════════════════════════════════════════════════════════╝
{self.COLORS['reset']}"""


class IPLocator:
    """Handles IP location data retrieval."""

    API_URL = "https://ipinfo.io/{}/json"

    def __init__(self, ip):
        self.ip = ip

    def get_data(self):
        """Fetch IP data from ipinfo.io."""
        try:
            headers = {
                "User-Agent": "Tinor-Shell-IPLocator/1.0"
            }

            response = requests.get(
                self.API_URL.format(self.ip),
                headers=headers,
                timeout=10
            )

            response.raise_for_status()
            data = response.json()

            if "error" in data:
                raise ValueError(
                    data["error"].get("message", "Unknown API error")
                )

            return data

        except requests.exceptions.RequestException as e:
            raise ConnectionError(
                f"Connection failed: {e}"
            ) from e


class OutputFormatter:
    """Handles formatted output."""

    def __init__(self, config):
        self.colors = config.COLORS
        self.banner = config.banner

    def show_banner(self):
        print(self.banner)

    def display_results(self, data):
        """Display IP location information."""

        lat = "N/A"
        lon = "N/A"

        if "loc" in data:
            lat_lon = data["loc"].split(",")

            if len(lat_lon) == 2:
                lat = lat_lon[0]
                lon = lat_lon[1]

        fields = [
            ("IP", data.get("ip", "N/A")),
            ("COUNTRY CODE", data.get("country", "N/A")),
            ("REGION", data.get("region", "N/A")),
            ("CITY", data.get("city", "N/A")),
            ("ZIP/POSTAL", data.get("postal", "N/A")),
            ("LATITUDE", lat),
            ("LONGITUDE", lon),
            ("TIME ZONE", data.get("timezone", "N/A")),
            ("ORG / ISP", data.get("org", "N/A")),
        ]

        if lat != "N/A" and lon != "N/A":
            google_map = f"https://www.google.com/maps?q={lat},{lon}"
        else:
            google_map = "N/A"

        print(
            f"\n{self.colors['grn']}"
            f"{' SECURE IP LOCATION INFORMATION ':-^60}"
            f"{self.colors['reset']}\n"
        )

        for display_name, value in fields:
            print(
                f"    {self.colors['grn']}"
                f"[{self.colors['red']}+{self.colors['grn']}] "
                f"{self.colors['lblue']}{display_name:<12} "
                f"{self.colors['red']}::: "
                f"{self.colors['ylw']}{value}"
            )

        print(
            f"\n    {self.colors['grn']}"
            f"[{self.colors['red']}+{self.colors['grn']}] "
            f"{self.colors['lblue']}GOOGLE MAP   "
            f"{self.colors['red']}::: "
            f"{self.colors['ylw']}{google_map}"
        )

        print(
            f"\n{self.colors['grn']}"
            f"{'-' * 60}"
            f"{self.colors['reset']}\n"
        )


def validate_ip(ip):
    """Validate IP and reject private/loopback addresses."""

    try:
        ip_obj = ipaddress.ip_address(ip)

        if ip_obj.is_private or ip_obj.is_loopback:
            return (
                False,
                "Cannot geolocate private or local loopback IPs."
            )

        return True, ""

    except ValueError:
        return False, "Invalid IP address format."


def find_info(ip):
    """
    Main function for Tinor Shell.

    Pass an IP address to this function:
        find_info("8.8.8.8")

    Returns the API data dictionary on success.
    Returns None on failure.
    """

    config = Config()
    formatter = OutputFormatter(config)

    # Validate IP
    is_valid, error_msg = validate_ip(ip)

    if not is_valid:
        print(
            f"\n{config.COLORS['red']}"
            f"Error: {error_msg}"
            f"{config.COLORS['reset']}"
        )
        return None

    try:
        print(f"\nLooking up IP: {ip}")

        locator = IPLocator(ip)
        data = locator.get_data()

        formatter.show_banner()
        formatter.display_results(data)

        return data

    except Exception as e:
        print(
            f"\n{config.COLORS['red']}"
            f"Error: {e}"
            f"{config.COLORS['reset']}"
        )
        return None


if __name__ == "__main__":
    ip = input("Enter IP address: ").strip()
    find_info(ip)