

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
            "animation": "./model/kogpt2_rg_naver_movie_20.ckpt"
        }


class TGConfig(Config):
    def __init__(self) -> None:
        super().__init__()
        self.model_dict = {
            "woongjin": "./model/kogpt2_tg_woongjin_15.ckpt"
        }


class CBConfig(Config):
    def __init__(self) -> None:
        super().__init__()
        self.model_dict = {

        }
