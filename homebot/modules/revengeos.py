from homebot import get_config
from homebot.logging import LOGE, LOGI, LOGD, LOGW
from homebot.modules_manager import register

# Module-specific imports
from datetime import datetime
import requests

DEVICES_JSON_URL = "https://raw.githubusercontent.com/RevengeOS-Devices/official_devices/master/maintainers.json"
DEVICE_SPECIFIC_JSON_URL = "https://raw.githubusercontent.com/RevengeOS-Devices/official_devices/master/{}/device.json"
DEFAULT_DONATION_LINK = "https://paypal.me/lucchetto"

def get_devices_json():
	try:
		response = requests.get(url=DEVICES_JSON_URL).json()
	except:
		response = None
	return response

def get_device_specific_json(device):
	try:
		response = requests.get(url=DEVICE_SPECIFIC_JSON_URL.format(device)).json()
	except:
		response = None
	return response

"""
@register(commands=['start'])
def start(update, context):
	update.message.reply_text("To get a list of the officially supported devices, type /devices")
"""

@register(commands=['device'])
def device(update, context):
	try:
		device = update.message.text.split()[1]
	except IndexError:
		update.message.reply_text("Error: Device codename not provided\n" + \
								  "Write a device codename after the command!\n" + \
								  "Example: /device whyred")
		return

	devices_json = get_devices_json()
	if devices_json is None:
		update.message.reply_text("Error: Devices JSON fetching failed, retry later")
		return

	for i in [device, device.lower(), device.upper()]:
		try:
			device_info = devices_json[i]
		except KeyError:
			device = None
		else:
			device = i
			break

	if device is None:
		update.message.reply_text("Error: Device codename is not present in RevengeOS official devices list!\n"
								  "Please make sure you wrote it correctly")
		return

	device_specific_json = get_device_specific_json(device)
	if device_specific_json is None:
		update.message.reply_text("Error: Device OTA JSON fetching failed, retry later")
		return

	try:
		release_date = datetime.utcfromtimestamp(device_specific_json["datetime"]).strftime('%Y-%m-%d')
	except ValueError:
		release_date = datetime.utcfromtimestamp(device_specific_json["datetime"] / 1000).strftime('%Y-%m-%d')

	try:
		update.message.reply_text('RevengeOS build for {}\n\n'.format(device) + \
								  'Name: {} {}\n'.format(device_info["brand"], device_info["name"]) + \
								  'Maintainer: {}\n'.format(device_info["maintainer"]) + \
								  'Donate: <a href="{}">Here</a>\n\n'.format(device_specific_json["donate_url"]) + \
								  'Latest version: <a href="{}">{}</a>\n'.format(device_specific_json["url"],
																			     device_specific_json["filename"]) + \
								  'Version: {}\n'.format(device_specific_json["version"]) + \
								  'Date: {}\n'.format(release_date),
								  parse_mode="HTML", disable_web_page_preview=True)
	except KeyError:
		update.message.reply_text("Error: Update message creation failed, please ask the maintainer to fix this")

@register(commands=['devices'])
def devices(update, context):
	devices_json = get_devices_json()
	if devices_json is None:
		update.message.reply_text("Error: Devices JSON fetching failed, retry later")
		return

	devices_list_sorted = sorted(devices_json, key=lambda x: (devices_json[x]['brand'], devices_json[x]['name']))
	message = "Supported devices:\n\n"
	for device in devices_list_sorted:
		message += "- {} {} ({})\n".format(devices_json[device]["brand"], devices_json[device]["name"], device)
	message += "To get the latest release for a device type /device <codename>"
	update.message.reply_text(message)
