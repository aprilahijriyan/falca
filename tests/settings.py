import os

_private = os.system

part_config = {"SATU": 1, "DUA": 2, "DICT": {"YO": 1, "MAN": "YOI"}}
full_config = {
    "FALCA_SATU": 1,
    "FALCA_DUA": 2,
    "FALCA_DICT": {"YO": 1, "MAN": "YOI"},
    **part_config,
}


class Config:
    pass


k, v = None, None
for k, v in full_config.items():
    setattr(Config, k, v)

del k, v
