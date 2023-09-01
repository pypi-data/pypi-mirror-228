#!/usr/bin/env python

"""Tests for `dwai` package."""
import unittest
import dwai
from datetime import datetime

from dwai.pangu.model_api.completions import PanGuCompletions
from dwai.tione.v20211111.tione_client import TioneClient
from dwai.bailian.model_api.completions import Completions

from dwai.zhipuai.model_api.api import ModelAPI
dwai.api_key = "dw-BBAa68XBJUqiIj6xUQcC0KREnqmt5mPKQ52wkylD-Tw"
dwai.api_base = "https://dwai.shizhuang-inc.com"


class TestDwai(unittest.TestCase):
    """Tests for `dwai` package."""

    def test_bailian_qa(self):
        """Test something."""
        chat = Completions()
        resp = chat.call(
            app_id="1e4ddc3659324ad0b8a0039230f1dba3",
            prompt="你好")
        print(resp)

    def test_bailian_qa_stream(self):
        chat = Completions()
        resp = chat.call(
            app_id="1e4ddc3659324ad0b8a0039230f1dba3",
            prompt="你好",
            stream=True)
        for line in resp:
            now = datetime.now()
            print("%s: %s" % (now, line), end="\n", flush=True)

    def test_zhipuai_invoke(self):
        model = ModelAPI()
        resp = model.invoke(
            model="chatglm_std",
            prompt=[{"role": "user", "content": "人工智能"}],
            top_p=0.7,
            temperature=0.9,
        )
        print(resp)

    def test_zhipuai_sse_invoke(self):
        model = ModelAPI()
        resp = model.sse_invoke(
            model="chatglm_std",
            prompt=[{"role": "user", "content": "人工智能"}],
            top_p=0.7,
            temperature=0.9,
        )
        for line in resp:
            now = datetime.now()
            print("%s: %s" % (now, line), end="\n", flush=True)

    def test_zhipuai_async_invoke(self):
        model = ModelAPI
        response = model.async_invoke(
            model="chatglm_std",
            prompt=[{"role": "user", "content": "人工智能"}],
            top_p=0.7,
            temperature=0.9,
        )
        print(response)

    def test_pangu(self):
        """Test something."""
        chat = PanGuCompletions()
        resp = chat.call(
            prompt="",
            max_tokens=600,
            messages=[{"role":"system","content":"请用幼儿园老师的口吻回答问题，注意语气温和亲切，通过提问、引导、赞美等方式，激发学生的思维和想象力。"},{"role":"user","content":"写一首诗"}],
            temperature=0.9,
            stream=True
        )
        # print(resp)
        for line in resp:
            now = datetime.now()
            print("%s: %s" % (now, line), end="\n", flush=True)

    def test_tione(self):
        """Test something."""
        chat = TioneClient()
        resp = chat.ChatCompletion(
            content="2+2=?"
        )
        print(resp)
