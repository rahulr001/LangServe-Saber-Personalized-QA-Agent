import sys


class CustomException:

    def __init__(self, error_detail, _sys: sys):
        _, _, exc_info = _sys.exc_info()
        file_name = exc_info.tb_frame.f_code.co_filename
        self.error_msg = f'{error_detail} in file [{file_name}] line number [{exc_info.tb_lineno}]'

    def __str__(self):
        return self.error_msg

