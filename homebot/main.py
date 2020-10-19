from homebot import updater, get_config
from homebot.logging import LOGE, LOGI, LOGD, LOGW
from homebot.modules_manager import init_modules

from homebot import __version__

def main():
	init_modules()
	try:
		updater.bot.get_me().username
	except:
		LOGE("Failed to connect to Telegram, check your internet connection and/or your bot token")
		exit()
	LOGI("HomeBot started, version " + str(__version__))
	LOGI("Bot username: @" + updater.bot.get_me().username)
	updater.start_polling()
