from nonebot import get_driver

from nonebot.plugin import PluginMetadata

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="星崽Bot-菜单",
    description="为星崽系列插件提供菜单",
    usage="能力中心",

    type="application",

    homepage="https://github.com/StarJian-Team/StarZai-Plugin/tree/Stable/Memu/NoneBot",

    config=Config,

    supported_adapters="~onebot.v11"
    # 支持的适配器集合，其中 `~` 在此处代表前缀 `nonebot.adapters.`，其余适配器亦按此格式填写。
    # 若插件可以保证兼容所有适配器（即仅使用基本适配器功能）可不填写，否则应该列出插件支持的适配器。
)

global_config = get_driver().config
config = Config.parse_obj(global_config)


from nonebot.rule import to_me
from nonebot.plugin import on_command
from nonebot.adapters.onebot.v11 import MessageSegment

# 能力中心 开始
memu = on_command("能力中心", rule=to_me(), aliases={"memu"}, priority=10, block=True)

@memu.handle()
async def handle_picture():
    # 构造图片消息段
    image = MessageSegment.image("https://img1.imgtp.com/2023/08/20/8HTWSxnz.png")
    # 发送图片
    await memu.send(image)
# 能力中心 结束
# 综合能力 开始
LittleGame = on_command("综合能力", rule=to_me(), aliases={"LittleGame"}, priority=10, block=True)

@LittleGame.handle()
async def handle_picture():
    # 构造图片消息段
    image = MessageSegment.image("https://img1.imgtp.com/2023/08/20/7s58il0g.png")
    # 发送图片
    await LittleGame.send(image)
# 综合能力 结束
# 其它能力 开始
Other = on_command("其它能力", rule=to_me(), aliases={"Other"}, priority=10, block=True)

@Other.handle()
async def handle_picture():
    # 构造图片消息段
    image = MessageSegment.image("https://img1.imgtp.com/2023/08/20/nBbqoN2L.png")
    # 发送图片
    await Other.send(image)
# 其它能力 结束