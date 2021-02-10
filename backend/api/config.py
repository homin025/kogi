

class Config:
    def __init__(self) -> None:
        self.model_dict: dict


class QGConfig(Config):
    def __init__(self) -> None:
        super().__init__()
        self.model_dict = {
            "korquad": "./model/kogpt2_qg_korquad_30.ckpt"
        }


class ASConfig(Config):
    def __init__(self) -> None:
        super().__init__()
        self.model_dict = {
            "korean": "./model/kogpt2_as_korean_50.ckpt"
        }


class RGConfig(Config):
    def __init__(self) -> None:
        super().__init__()
        self.model_dict = {
            "naver": "./model/kogpt2_rg_naver_23.ckpt",
            "ogeoseo_25": "./model/kogpt2_rg_ogeoseo_25.ckpt",
            "ogeoseo_50": "./model/kogpt2_rg_ogeoseo_50.ckpt"
        }


class TGConfig(Config):
    def __init__(self) -> None:
        super().__init__()
        self.model_dict = {
            "woongjin": "./model/kogpt2_tg_woongjin_13.ckpt"
        }


class CBConfig(Config):
    def __init__(self) -> None:
        super().__init__()
        self.model_dict = {

        }
