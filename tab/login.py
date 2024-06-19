import gradio as gr
from loguru import logger

from config import main_request, configDB, global_cookieManager
from util.KVDatabase import KVDatabase

names = []


@logger.catch
def login_tab():
    gr.Markdown("""
> **补充**
>
> 在这里，你可以
> 1. 去更改账号，
> 2. 查看当前程序正在使用哪个账号
> 3. 使用配置文件切换到另一个账号
>
""")
    with gr.Row():
        username_ui = gr.Text(
            main_request.get_request_name(),
            label="账号名称",
            interactive=False,
            info="当前账号的名称",
        )
        gr_file_ui = gr.File(label="当前登录信息文件",
                             value=configDB.get("cookie_path"))
    gr.Markdown("""🏵️ 登录""")
    info_ui = gr.TextArea(
        info="此窗口为输出信息", label="输出信息", interactive=False
    )

    with gr.Row():
        upload_ui = gr.UploadButton(label="导入")
        add_btn = gr.Button("注销并重新登录")

        def upload_file(filepath):
            main_request.cookieManager.db.delete("cookie")
            yield ["已经注销，请选择登录信息文件", gr.update(), gr.update()]
            try:
                configDB.insert("cookie_path", filepath)
                global_cookieManager.db = KVDatabase(filepath)
                name = main_request.get_request_name()
                yield [gr.update(value="导入成功"), gr.update(value=name), gr.update(value=configDB.get("cookie_path"))]
            except Exception:
                name = main_request.get_request_name()
                yield ["登录出现错误", gr.update(value=name), gr.update(value=configDB.get("cookie_path"))]

        upload_ui.upload(upload_file, [upload_ui], [info_ui, username_ui, gr_file_ui])

        def add():
            main_request.cookieManager.db.delete("cookie")
            yield ["已经注销，将打开浏览器，请在浏览器里面重新登录", gr.update(value="未登录"),
                   gr.update(value=configDB.get("cookie_path"))]
            try:
                main_request.cookieManager.get_cookies_str_force()
                name = main_request.get_request_name()
                yield [f"登录成功", gr.update(value=name), gr.update(value=configDB.get("cookie_path"))]
            except Exception:
                name = main_request.get_request_name()
                yield ["登录出现错误", gr.update(value=name), gr.update(value=configDB.get("cookie_path"))]

        add_btn.click(
            fn=add,
            inputs=None,
            outputs=[info_ui, username_ui, gr_file_ui]
        )
