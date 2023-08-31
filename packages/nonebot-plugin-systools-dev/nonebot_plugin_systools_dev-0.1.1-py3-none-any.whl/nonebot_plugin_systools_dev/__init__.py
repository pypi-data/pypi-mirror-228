import nonebot
from nonebot import on_command #引入on_command参数（必须）
from nonebot.adapters import Message #引入消息数组
from nonebot.params import CommandArg #引入消息分词
配置 = nonebot.get_driver().config
command_starts = list(nonebot.get_driver().config.command_start)
default_start = command_starts[0]

from nonebot.plugin import PluginMetadata

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="系统助手-Dev",
    description="系统助手 for Nonebot - 支持运行系统命令、备份 Koishi 配置文件到 GitHub、查询系统状态、获取 IP 地址等进阶操作",
    usage="系统助手",

    type="application",

    homepage="https://github.com/zhuhansan666/nonebot-plugin-systools/tree/Dev_for_shanshui",

    config=Config,

    supported_adapters={"~onebot.v11"}
    # 支持的适配器集合，其中 `~` 在此处代表前缀 `nonebot.adapters.`，其余适配器亦按此格式填写。
    # 若插件可以保证兼容所有适配器（即仅使用基本适配器功能）可不填写，否则应该列出插件支持的适配器。
)


systool = on_command("systool")
@systool.handle()
async def handle_function(args: Message = CommandArg()):
    内容 = args.extract_plain_text()  #取命令后跟的内容
    if 内容 := 内容:
        if 内容 == "help":
            return 0
    else:
        await systool.send("您好像没有添加任何参数，已默认输出帮助菜单")
        await systool.finish(f'''Systools帮助菜单
{default_start}systool  #Systools菜单
{default_start}systool ''')