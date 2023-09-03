# Copyright 2023 Nguyen Phuc Binh @ GitHub
# See LICENSE for details.
__version__ = "2.1.8"
__author__ ="Nguyen Phuc Binh"
__copyright__ = "Copyright 2023, Nguyen Phuc Binh"
__license__ = "MIT"
__email__ = "nguyenphucbinh67@gmail.com"
__website__ = "https://github.com/NPhucBinh"

from . import user_agent
#from . import data_cafef
#from . import cafef_test
from .stockvn import (report_finance_cf, get_data_history_cafef,
    getCPI_vietstock,solieu_GDP_vietstock, laisuat_vietstock, exchange_currency, tygia_vietstock, 
    solieu_XNK_vietstock, solieu_tindung_vietstock, solieu_sanxuat_congnghiep, solieu_banle_vietstock, solieu_danso_vietstock,solieu_FDI_vietstock)