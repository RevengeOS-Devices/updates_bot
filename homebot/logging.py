from inspect import currentframe
from logging import basicConfig, debug, info, error, warning, INFO

basicConfig(format='%(asctime)s [%(levelname)s] %(message)s',
					level=INFO)

def LOGD(message):
	debug(currentframe().f_back.f_code.co_name + ": " + message)

def LOGI(message):
	info(currentframe().f_back.f_code.co_name + ": " + message)

def LOGE(message):
	error(currentframe().f_back.f_code.co_name + ": " + message)

def LOGW(message):
	warning(currentframe().f_back.f_code.co_name + ": " + message)
