

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
            "kogpt2": "./model/kogpt2_model.params",
            "naver_movie": "./model/kogpt2_rg_naver_movie_20.ckpt"
        }


class TGConfig(Config):
    def __init__(self) -> None:
        super().__init__()
        self.model_dict = {
            "kogpt2": "./model/kogpt2_model.params",
            "woongjin_books": "./model/kogpt2_tg_woongjin_books_70.ckpt",
            "aesop_fables": "./model/kogpt2_tg_aesop_fables_20.ckpt"
        }


class CBConfig(Config):
    def __init__(self) -> None:
        super().__init__()
        self.model_dict = {

        }
