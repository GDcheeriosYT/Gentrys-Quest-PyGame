from Localization.Language import Language


class Japanese(Language):
    def __init__(self):
        super().__init__(
            "日本語",
            play="あそぶ",
            settings="設定",
            back="返す",
            done="ダン",
            next="次",
            confirm="正す",
            guest="客",
            username="ユーザー名",
            create_guest="客を作ります",
            login="ログイン",
            login_not_available="ログインを出来ません。。。",
            audio="音響",
            graphics="グラフィックス",
            music="歌",
            music_volume="歌の音量",
            sound="音",
            sound_volume="音の音量",
            volume="音量",
            fullscreen="フールスクリン",
            extra_ui_info="追加のUI情報",
            apply="適用する",
            applied_settings="設定を適用しました",
            inventory="在庫",
            characters="人",
            character="一人",
            artifacts="物",
            weapons="武器",
            weapon="武器",
            changelog="変更のリスト",
            travel="旅行する",
            gacha="ガチャ",
            equip="装備する",
            upgrade="磨く",
            upgrade_with_weapons="武器で磨く",
            not_number_error="数じゃないです",
            cant_afford="高すぎる"
        )