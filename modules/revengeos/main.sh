#!/bin/bash
#
# Copyright (C) 2020 SebaUbuntu's HomeBot
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

parse_ota() {
	local REVENGEOS_GENERIC_JSON="$(curl https://raw.githubusercontent.com/RevengeOS-Devices/official_devices/r10.0/maintainers.json | jq .)"
	if echo "$1" | grep -q "-"; then
		echo "$REVENGEOS_GENERIC_JSON" | jq '.["$1"]'
	else
		echo "$REVENGEOS_GENERIC_JSON" | jq ".$1"
	fi
}

module_device() {
	# Trim codename
	local DEVICE_CODENAME="$(tg_get_command_arguments "$@" | sed 's/[^0-9a-zA-Z_-]*//g')"
	if [ "$DEVICE_CODENAME" != "" ]; then
		local REVENGEOS_DEVICE_JSON=$(parse_ota "$DEVICE_CODENAME")
		if [ "$REVENGEOS_DEVICE_JSON" = "null" ]; then
			# Try lowercase codename
			local DEVICE_CODENAME=$(echo $DEVICE_CODENAME | tr '[:upper:]' '[:lower:]')
			local REVENGEOS_DEVICE_JSON=$(parse_ota "$DEVICE_CODENAME")
		fi
		if [ "$REVENGEOS_DEVICE_JSON" = "null" ]; then
			# Try uppercase codename
			local DEVICE_CODENAME=$(echo $DEVICE_CODENAME | tr '[:lower:]' '[:upper:]')
			local REVENGEOS_DEVICE_JSON=$(parse_ota "$DEVICE_CODENAME")
		fi
		REVENGEOS_DEVICE_UPDATE_JSON="$(curl https://raw.githubusercontent.com/RevengeOS-Devices/official_devices/r10.0/$DEVICE_CODENAME/device.json | jq .)"
		if [ "$REVENGEOS_DEVICE_JSON" != "null" ] && [ "$(echo "$REVENGEOS_DEVICE_UPDATE_JSON" | jq ".filename" | cut -d "\"" -f 2)" != "" ]; then
			local REVENGEOS_DEVICE_INFO="RevengeOS Q build for $DEVICE_CODENAME

Name: $(echo "$REVENGEOS_DEVICE_JSON" | jq ".name" | cut -d "\"" -f 2)
Mantainer: $(echo "$REVENGEOS_DEVICE_JSON" | jq ".maintainer" | cut -d "\"" -f 2)
Latest version: [$(echo "$REVENGEOS_DEVICE_UPDATE_JSON" | jq ".filename" | cut -d "\"" -f 2)]($(echo "$REVENGEOS_DEVICE_UPDATE_JSON" | jq ".url" | cut -d "\"" -f 2))"
			if [ "$(echo "$REVENGEOS_DEVICE_JSON" | jq ".xda_thread" | cut -d "\"" -f 2)" != "" ]; then
				local REVENGEOS_DEVICE_INFO="$REVENGEOS_DEVICE_INFO
XDA thread: [Here]($(echo "$REVENGEOS_DEVICE_JSON" | jq ".xda_thread" | cut -d "\"" -f 2))"
			fi
			if [ "$(echo "$REVENGEOS_DEVICE_UPDATE_JSON" | jq ".donate_url" | cut -d "\"" -f 2)" != "" ]; then
				local REVENGEOS_DEVICE_INFO="$REVENGEOS_DEVICE_INFO
Donate: [Here]($(echo "$REVENGEOS_DEVICE_UPDATE_JSON" | jq ".donate_url" | cut -d "\"" -f 2))"
			else
				local REVENGEOS_DEVICE_INFO="$REVENGEOS_DEVICE_INFO
Donate: [Here](https://paypal.me/lucchetto)"
			fi
			tg_send_message "$(tg_get_chat_id "$@")" "$REVENGEOS_DEVICE_INFO" "$(tg_get_message_id "$@")"
		else
			tg_send_message "$(tg_get_chat_id "$@")" "Device codename is not present in RevengeOS official devices list!
Please make sure you wrote it correctly" "$(tg_get_message_id "$@")"
		fi
	else
		tg_send_message "$(tg_get_chat_id "$@")" "Please write a device codename!" "$(tg_get_message_id "$@")"
	fi
}

module_devices() {
	local REVENGEOS_GENERIC_JSON="$(curl https://raw.githubusercontent.com/RevengeOS-Devices/official_devices/r10.0/maintainers.json | jq .)"
	local REVENGEOS_DEVICES_LIST="$(echo "$REVENGEOS_GENERIC_JSON" | jq 'to_entries | .[].key' | cut -d "\"" -f 2)"
	local REVENGEOS_DEVICES_MESSAGE="List of RevengeOS official supported devices:
"
	for device in $(echo "$REVENGEOS_DEVICES_LIST"); do
		local REVENGEOS_DEVICES_MESSAGE="$REVENGEOS_DEVICES_MESSAGE
$(echo $REVENGEOS_GENERIC_JSON | jq ".$device.name" | cut -d "\"" -f 2)  (\`$device\`)"
	done
	local REVENGEOS_DEVICES_MESSAGE="$REVENGEOS_DEVICES_MESSAGE
	
To get the last release for a device type /device <codename>"
	tg_send_message "$(tg_get_chat_id "$@")" "$REVENGEOS_DEVICES_MESSAGE" "$(tg_get_message_id "$@")"
}