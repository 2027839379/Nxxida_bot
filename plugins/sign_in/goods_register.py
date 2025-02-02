import nonebot
from nonebot import Driver

from configs.config import Config
from models.sign_group_user import SignGroupUser
from utils.decorator.shop import NotMeetUseConditionsException, shop_register

driver: Driver = nonebot.get_driver()


@driver.on_startup
async def _():
    """
    导入内置的三个商品
    """

    @shop_register(
        name=("好感度双倍加持卡Ⅰ", "好感度双倍加持卡Ⅱ", "好感度双倍加持卡Ⅲ", "好感度双倍加持卡Ⅳ", "好感度双倍加持卡Ⅴ", "好感度双倍加持卡Ⅵ", "好感度双倍加持卡Ⅶ", "好感度双倍加持卡Ⅷ", "好感度双倍加持卡Ⅸ", "好感度双倍加持卡Ⅹ"),
        price=(30, 150, 250, 500, 750, 1000, 1500, 4000, 6000, 10000),
        des=(
            "下次签到双倍好感度概率 + 10%（谁才是真命天子？）（同类商品将覆盖）",
            "下次签到双倍好感度概率 + 20%（平平庸庸）（同类商品将覆盖）",
            "下次签到双倍好感度概率 + 30%（金币才是真命天子！）（同类商品将覆盖）",
            "下次签到双倍好感度概率 + 40%",
            "下次签到双倍好感度概率 + 50%",
            "下次签到双倍好感度概率 + 60%",
            "下次签到双倍好感度概率 + 70%",
            "下次签到双倍好感度概率 + 80%",
            "下次签到双倍好感度概率 + 90%（还差一点点）",
            "下次签到双倍好感度概率 + 100%(我就是天命)",
        ),
        load_status=bool(Config.get_config("shop", "IMPORT_DEFAULT_SHOP_GOODS")),
        icon=(
            "favorability_card_1.png",
            "favorability_card_2.png",
            "favorability_card_3.png",
            "favorability_card_4.png",
            "favorability_card_5.png",
            "favorability_card_6.png",
            "favorability_card_7.png",
            "favorability_card_8.png",
            "favorability_card_9.png",
            "favorability_card_10.png",
        ),
        **{"好感度双倍加持卡Ⅰ_prob": 0.1, "好感度双倍加持卡Ⅱ_prob": 0.2, "好感度双倍加持卡Ⅲ_prob": 0.3, "好感度双倍加持卡Ⅳ_prob": 0.4, "好感度双倍加持卡Ⅴ_prob": 0.5, "好感度双倍加持卡Ⅵ_prob": 0.6, "好感度双倍加持卡Ⅶ_prob": 0.7, "好感度双倍加持卡Ⅷ_prob": 0.8, "好感度双倍加持卡Ⅸ_prob": 0.9, "好感度双倍加持卡Ⅹ_prob": 1.0},
    )
    async def sign_card(user_id: int, group_id: int, prob: float):
        user, _ = await SignGroupUser.get_or_create(user_id=str(user_id), group_id=str(group_id))
        user.add_probability = prob
        await user.save(update_fields=["add_probability"])

    @shop_register(
        name="测试道具A",
        price=99,
        des="随便侧而出",
        load_status=False,
        icon="sword.png",
    )
    async def _(user_id: int, group_id: int):
        print(user_id, group_id, "使用测试道具")

    @shop_register.before_handle(name="测试道具A", load_status=False)
    async def _(user_id: int, group_id: int):
        print(user_id, group_id, "第一个使用前函数（before handle）")

    @shop_register.before_handle(name="测试道具A", load_status=False)
    async def _(user_id: int, group_id: int):
        print(user_id, group_id, "第二个使用前函数（before handle）222")
        raise NotMeetUseConditionsException("太笨了！")  # 抛出异常，阻断使用，并返回信息

    @shop_register.after_handle(name="测试道具A", load_status=False)
    async def _(user_id: int, group_id: int):
        print(user_id, group_id, "第一个使用后函数（after handle）")
