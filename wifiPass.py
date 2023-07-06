import subprocess
import sys
import logging


def get_wifi_profiles():
    try:
        output = subprocess.check_output(['nmcli', '-t', '-f', 'name', 'connection', 'show', '--active'],
                                         stderr=subprocess.DEVNULL)
        profiles = output.decode('utf-8').strip().split('\n')
        return [profile for profile in profiles if profile]
    except FileNotFoundError:
        logging.error("nmcli command not found. Make sure nmcli is installed and accessible in the system's PATH.")
        sys.exit(1)
    except subprocess.CalledProcessError:
        logging.error("Error occurred while retrieving Wi-Fi profiles.")
        sys.exit(1)


def retrieve_password(profile):
    try:
        output = subprocess.check_output(['nmcli', '-s', '-g', '802-11-wireless-security.psk', 'connection', 'show',
                                          profile], stderr=subprocess.DEVNULL)
        password = output.decode('utf-8').strip()
        if password:
            return password
        else:
            return None
    except subprocess.CalledProcessError:
        return None


def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(message)s')


def main():
    setup_logging()
    wifi_profiles = get_wifi_profiles()

    for profile in wifi_profiles:
        password = retrieve_password(profile)
        if password:
            logging.info(f"Wi-Fi Profile: {profile}, Password: {password}")
        else:
            logging.info(f"Wi-Fi Profile: {profile}, Password: Not available")


if __name__ == '__main__':
    main()
