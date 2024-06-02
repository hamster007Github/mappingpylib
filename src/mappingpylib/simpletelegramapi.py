#!/usr/local/bin/python
# -*- coding: utf-8 -*-

'''
****************************************
* Import
****************************************
'''
import json
# url handling
import urllib
import requests
# logging
import logging

'''
****************************************
* Global variables
****************************************
'''
log = logging.getLogger(__name__)
MAX_MSG_LEN = 3000
ERROR_DESC_NO_MODIFICATION = "Bad Request: message is not modified: specified new message content and reply markup are exactly the same as a current content and reply markup of the message"

'''
****************************************
* Classes
****************************************
'''
class CommunicationError(Exception):
    pass

class SimpleTelegramApi:
    def __init__(self, api_token:str) -> None:
        self._base_url = self._get_base_url(api_token)

    def _get_base_url(self, api_token:str) -> str:
        """get TG bot API base url including bot token"""

        return "https://api.telegram.org/bot{}/".format(api_token)

    def _send_request(self, command:str) -> dict:
        """send TG bot API https request and return https response"""

        request_url = self._base_url + command
        try:
            response = requests.get(request_url)
            decoded_response = json.loads(response.content.decode("utf8"))
        except Exception as error:
            # most likely telegram server or internet connection issue
            raise CommunicationError(f"{error}")
        return decoded_response

    def _limit_text_len(self, text:str) -> str:
        """trim text to <= MAX_MSG_LEN"""

        if len(text) > MAX_MSG_LEN:
            # trim to max len - trim_end_str
            trimmed_text = text[:(MAX_MSG_LEN-1)]
        else:
            trimmed_text = text
        return trimmed_text

    def _create_send_msg_request(self, chat_id:str, text:str, parse_mode:str, disable_web_page_preview:bool = True) -> str:
        """create a telegram bot API url request string"""

        text = urllib.parse.quote_plus(self._limit_text_len(text))
        request = f"sendMessage?text={text}&chat_id={chat_id}&parse_mode={parse_mode}&disable_web_page_preview={disable_web_page_preview}"
        return request

    def _create_edit_msg_request(self, chat_id:str, message_id:str, text:str, parse_mode:str, disable_web_page_preview:bool = True) -> str:
        """create a telegram bot API url request string"""

        text = urllib.parse.quote_plus(self._limit_text_len(text))
        request = f"editMessageText?chat_id={chat_id}&message_id={message_id}&parse_mode={parse_mode}&disable_web_page_preview={disable_web_page_preview}&text={text}"
        return request

    @staticmethod
    def _is_response_ok(response:dict) -> bool:
        """check response of a message and return interpretation"""

        result = False
        try:
            if isinstance(response, dict):
                if not response["ok"]:
                    error_code = response["error_code"]
                    description = response["description"]
                    if error_code == 400 and description == ERROR_DESC_NO_MODIFICATION:
                        result = True
                    else:
                        result = False
                else:
                    result = True
        except Exception:
            log.exception("Can't check_response. Response seems not matching with TG API.")
            result = False
        return result

    @staticmethod
    def util_smart_trim_text(text:str, trim_end_str:str="...", trim_str:str="\n") -> str:
        """smart trim text to <= MAX_MSG_LEN until next trim_str substring (default: new line) was found.
        Insert a trim_end_str substring at the end of the text to mark text as trimmed."""

        if len(text) > MAX_MSG_LEN:
            # trim to max len - trim_end_str
            trimmed_text = text[:(MAX_MSG_LEN-len(trim_end_str))]
            # trim to last found trim_str
            index = trimmed_text.rfind(trim_str)
            trimmed_text = trimmed_text[:index]
            # mark trimmed message with trim_end_str substring
            trimmed_text += trim_end_str
        else:
            trimmed_text = text
        return trimmed_text

    def send_message(self, chat_id:str, text:str, parse_mode="HTML") -> tuple[bool, int | None]:
        """send a new text message into a chat"""

        return_success = False
        return_message_id = None
        try:
            request = self._create_send_msg_request(chat_id, text, parse_mode)
            response = self._send_request(request)
            if SimpleTelegramApi._is_response_ok(response):
                return_message_id = response["result"]["message_id"]
                return_success = True
            else:
                log.warning(f"send_message failed for chat_id:'{chat_id}'. response:{response}")
        except CommunicationError as error:
            log.warning(f"send_message(): CommunicationError: {error}")
            return_success = True
            return_message_id = None
        except Exception as error:
            log.exception(f"send_message(): unexpected Exception: {error}")
            return_success = False
            return_message_id = None
        return return_success, return_message_id

    def send_message_thread(self, chat_id:str, message_thread_id:int, text:str, parse_mode="HTML") -> tuple[bool, int | None]:
        """send a new text message into a topic(message thread) of a chat"""

        return_success = False
        return_message_id = None
        try:
            request = self._create_send_msg_request(chat_id, text, parse_mode)
            request += f"&message_thread_id={message_thread_id}"
            response = self._send_request(request)
            if SimpleTelegramApi._is_response_ok(response):
                return_message_id = response["result"]["message_id"]
                return_success = True
            else:
                log.warning(f"send_message_thread failed for chat_id:'{chat_id}' message_thread_id:'{message_thread_id}'. response:{response}")
        except CommunicationError as error:
            log.warning(f"send_message_thread(): CommunicationError: {error}")
            return_success = True
            return_message_id = None
        except Exception as error:
            log.exception(f"send_message_thread(): unexpected Exception: {error}")
            return_success = False
            return_message_id = None
        return return_success, return_message_id

    def edit_message(self, chat_id:str, message_id:int, text:str, parse_mode="HTML") -> bool:
        """edit a text message from a chat"""

        return_success = False
        try:
            request = self._create_edit_msg_request(chat_id, message_id, text, parse_mode)
            response = self._send_request(request)
            if SimpleTelegramApi._is_response_ok(response):
                return_success = True
            else:
                log.warning(f"edit_message failed for chat_id:'{chat_id}'. response:{response}")
        except CommunicationError as error:
            log.warning(f"edit_message(): CommunicationError: {error}")
            return_success = True
        except Exception as error:
            log.exception(f"edit_message(): unexpected Exception: {error}")
            return_success = False
        return return_success

    def delete_message(self, chat_id:str, message_id:int) -> bool:
        """delete a message from a chat"""

        return_success = False
        try:
            response = self._send_request("deleteMessage?chat_id={}&message_id={}".format(chat_id, message_id))
            if SimpleTelegramApi._is_response_ok(response):
                return_success = True
            else:
                log.warning(f"delete_message failed for chat_id:'{chat_id}'. response:{response}")
        except CommunicationError as error:
            log.warning(f"edit_message(): CommunicationError: {error}")
            return_success = True
        except Exception as error:
            log.exception(f"edit_message(): unexpected Exception: {error}")
            return_success = False
        return return_success

    def pin_message(self, chat_id:str, message_id:int, disable_notification:bool="True") -> bool:
        """pin a message in a chat"""

        return_success = False
        try:
            response = self._send_request("pinChatMessage?chat_id={}&message_id={}&disable_notification={}".format(chat_id, message_id, disable_notification))
            if SimpleTelegramApi._is_response_ok(response):
                return_success = True
            else:
                log.warning(f"pin_message failed for chat_id:'{chat_id}'. response:{response}")
        except CommunicationError as error:
            log.warning(f"edit_message(): CommunicationError: {error}")
            return_success = True
        except Exception as error:
            log.exception(f"edit_message(): unexpected Exception: {error}")
            return_success = False
        return return_success
