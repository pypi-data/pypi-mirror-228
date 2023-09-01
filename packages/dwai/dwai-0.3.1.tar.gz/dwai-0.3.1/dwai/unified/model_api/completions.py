import json

from dwai.bailian.model_api.completions import Completions
from dwai.pangu.model_api.completions import PanGuCompletions
from dwai.tione.v20211111.tione_client import TioneClient
from dwai.zhipuai.model_api.api import ModelAPI
from jsonpath_ng import parse


def dwai_bailian_qa(**kwargs):
    chat = Completions()
    json = chat.call(app_id="1e4ddc3659324ad0b8a0039230f1dba3", prompt=kwargs.get('prompt'))
    jsonpath_expr = parse('$.output.text')
    matches = jsonpath_expr.find(json)
    if len(matches) > 0:
        return {
            "output": {"text": matches[0].value},
            "Success": True
        }
    else:
        return {}


# {
#     "output": {
#         "finish_reason": "stop",
#         "text": "你好！有什么我能为你效劳的吗？"
#     },
#     "usage": {
#         "output_tokens": 15,
#         "input_tokens": 21
#     },
#     "request_id": "a04ab7d9-3a26-9963-a0dd-dfa444e80b16"
# }

def zhipuai_chatglm_std(**kwargs):
    model = ModelAPI()
    json = model.invoke(model="chatglm_std", prompt=[{"role": "user", "content": kwargs.get('prompt')}],
                        top_p=kwargs.get('top_p', 0.7), temperature=kwargs.get('temperature', 0.9))
    jsonpath_expr = parse('$.data.choices[0].content')
    matches = jsonpath_expr.find(json)
    if len(matches) > 0:
        return {
            "output": {"text": matches[0].value},
            "Success": True
        }
    else:
        return {}


# {'code': 200, 'msg': '操作成功', 'data': {'request_id': '7890109047407633991', 'task_id': '7890109047407633991', 'task_status': 'SUCCESS', 'choices': [{'role': 'assistant', 'content': '" 人工智能（Artificial Intelligence，简称 AI）是一门研究、开发模拟、延伸和扩展人类智能的理论、方法、技术及应用系统的新兴技术科学。它是计算机科学的一个重要分支，涉及机器人、语言识别、图像识别、自然语言处理和专家系统等多个领域。人工智能的目的是生产具有类似人类智能的智能机器，能够以类似人类的方式进行反应和思考。\\n\\n人工智能的发展对各个领域产生了深远的影响，包括机器翻译、智能控制、专家系统、机器人学、语言和图像理解、遗传编程机器人工厂、自动程序设计、航天应用、庞大的信息处理、储存与管理，以及执行复杂或规模庞大的任务等。\\n\\n人工智能的意义在于，它为人类提供了一种可能性，即通过高度发展的技术手段，模拟和扩展人类智能，从而在很大程度上减轻人类的负担，提高工作效率，解决复杂问题，以及实现人类无法完成的任务。同时，人工智能的发展也对马克思主义哲学意识论提供了一种证明，表明意识可以在高度发展的物质中得以实现。"'}], 'usage': {'total_tokens': 214}}, 'success': True}


def pangu_completions(**kwargs):
    chat = PanGuCompletions()
    json = chat.call(max_tokens=kwargs.get('max_tokens', 600), prompt="",
                     messages=[{"role": "user", "content": kwargs.get('prompt')}],
                     temperature=kwargs.get('temperature', 0.9))
    jsonpath_expr = parse('$.choices[0].message.content')
    matches = jsonpath_expr.find(json)
    if len(matches) > 0:
        return {
            "output": {"text": matches[0].value},
            "Success": True
        }
    else:
        return {}


# {
#     "id": "72cc690126d6bb372d9e667604762c80",
#     "created": 20230829122227,
#     "choices": [
#         {
#             "index": 0,
#             "message": {
#                 "content": "春天来了,花儿开放了\n小草儿也长出来了\n小鸟在枝头唱着歌\n孩子们快乐地奔跑着"
#             }
#         }
#     ],
#     "usage": {
#         "completion_tokens": 28,
#         "prompt_tokens": 120,
#         "total_tokens": 148
#     }
# }

def tione_chat_completion(**kwargs):
    chat = TioneClient()
    content = chat.ChatCompletion(content=kwargs.get('prompt')).to_json_string()
    json_obj = json.loads(content)
    jsonpath_expr = parse('$.Choices[0].Message.Content')
    matches = jsonpath_expr.find(json_obj)
    if len(matches) > 0:
        return {
            "output": {"text": matches[0].value},
            "Success": True
        }
    else:
        return {}


# {
#     "Model": "tj_llm_clm-v1",
#     "Choices": [
#         {
#             "Message": {
#                 "Role": "assistant",
#                 "Content": "2+2 等于 4。"
#             },
#             "FinishReason": "",
#             "Index": 0
#         }
#     ],
#     "RequestId": "16496d8c-1900-46ec-b0c4-6ee578e4ad55"
# }

class UnifiedSDK:
    def __init__(self):
        self.route_map = {
            'alibaba.qwen-plus-v1': dwai_bailian_qa,
            'kingsoft.default': zhipuai_chatglm_std,
            'huawei.default': pangu_completions,
            'tencent.default': tione_chat_completion
        }

    def call(self, model_key, **kwargs):
        func = self.route_map.get(model_key)
        if func:
            return func(**kwargs)
        else:
            raise ValueError(f"Unknown model_key: {model_key}")


import dwai

dwai.api_key = "dw-BBAa68XBJUqiIj6xUQcC0KREnqmt5mPKQ52wkylD-Tw"
dwai.api_base = "https://dwai.shizhuang-inc.com"

if __name__ == '__main__':
    sdk = UnifiedSDK()

    # 测试dwai
    resp = sdk.call('alibaba.qwen-plus-v1', prompt="你好")
    print(resp)

    # 测试zhipuai
    resp = sdk.call('kingsoft.default', prompt="人工智能是什么", top_p=0.7, temperature=0.9)
    print(resp)

    # 测试pangu
    resp = sdk.call('huawei.default', prompt="写一首诗", max_tokens=600, temperature=0.9)
    print(resp)

    # 测试tione
    resp = sdk.call('tencent.default', prompt="2+2=?")
    print(resp)
