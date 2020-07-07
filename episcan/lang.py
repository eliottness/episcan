class Lang:
    UnK = 0
    RAW = 1
    VUS = 2
    VF = 3

    from_int = [UnK, RAW, VUS, VF]
    to_str   = ["Unknown lang", "RAW", "VUS", "VF"]

    @staticmethod
    def get_lang(lang):
        if isinstance(lang, Lang):
            return lang
        elif type(lang) is int and lang >= 0 and lang < len(Lang.from_int):
            return Lang.from_int[lang]
        else:
            raise TypeError(
                f"Language must be either of type {repr(Lang)} or of type int")
