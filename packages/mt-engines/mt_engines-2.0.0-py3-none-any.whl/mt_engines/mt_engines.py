import requests
import json
import time
from tencentcloud.common import credential
from tencentcloud.tmt.v20180321 import tmt_client, models
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
from deep_translator import GoogleTranslator
from itertools import chain
import re

class MTTranslator:
    """机翻类，所有的翻译功能由translate和translate_batch提供。他们会调用创建的MTEngine来执行翻译，其中translate_batch自动提供了平衡输入的功能，尽可能最大化每次请求的数据量，但是相应需要减少请求的线程数"""
    def __init__(self, engine_name: str, **kwargs) -> None:
        """Parameters
        ----------
        engine_name : {'Google', 'Tencent', 'Deepl'}, default 'Google
        '"""
        try:
            self.engine: MTEngine = globals()[engine_name]
        except:
            raise NameError("没有指定的翻译引擎")
        self.engine = self.engine(**kwargs)
        self.book = None
    
    @property
    def support_languages(self):
        return self.engine.support_languages()
    
    @classmethod
    @property
    def engine_list(cls):
        return ['Google', 'Tencent', 'Deepl']

    def translate(self, text, source, target, interval=0):
        if pd.isna(text):
            return text
        elif not isinstance(text, str):
            return text
        elif text.strip() == "":
            return text
        else:
            return self.engine.translate(text, source, target, interval)

    def _translate_batch(self, text_list, source, target, interval=0):
        return self.engine.translate_batch(text_list, source, target, interval)
    
    def pool_translate(
        self, text_list: list, source: str, target: str, thread_num=3, interval=1, batch=False
    ):
        """开启batch后的输入值是嵌套列表，每单个请求都传入了一个列表"""
        list_length = len(text_list)
        source = [source] * list_length
        target = [target] * list_length
        interval = [interval] * list_length
        if batch:
            func = self._translate_batch
        else:
            func = self.translate

        with ThreadPoolExecutor(max_workers=thread_num) as executor:
            results = executor.map(func, text_list, source, target, interval)

        if batch:
            results = chain(*results)

        return list(results)

    def compress_translate(self, text_list:list, source: str, target: str, thread_num=4, max_words=2000, interval=1):
        """调节单词文本上传大小，使效率最大化"""
        text_series = pd.Series(text_list).fillna('').astype(str)
        refer = text_series.str.len().cumsum().floordiv(max_words).astype(int)
        prepared_list = [row.to_list() for i, row in text_series.groupby(refer)]
        trans = self.pool_translate(prepared_list, source, target, thread_num, interval, True)
        return trans
    
    def load_file(self, path, **kwargs):
        if path.endswith('csv'):
            df = pd.read_csv(path,**kwargs)
        else:
            df = pd.read_excel(path, **kwargs)
        self.book = df.fillna('').astype(str)
        return self.book
    
    def translate_file(self, source_lang, target_lang, file_settings=(1,'auto',1,2), compress=False):
        """Parameters
        ----------
        file_settings : 由起始行，终止行，原文列，译文列组成的元组，终止行可以设置为auto，其他都是int。
        '"""
        file_settings = list(file_settings)
        if isinstance(file_settings[1],str):
            file_settings[1]=self.book.shape[0]
        if file_settings[3]==self.book.shape[1]:
            self.book['新增翻译']=None
        elif file_settings[3]>self.book.shape[1]:
            raise IndexError('译文列超出表格大小')
        else:
            ...
        text_list = self.book.iloc[file_settings[0]:file_settings[1],file_settings[2]].to_list()
        if compress:
            result = self.compress_translate(text_list, source_lang, target_lang)
        else:
            result = self.pool_translate(text_list, source_lang, target_lang)
        
        self.book.iloc[file_settings[0]:file_settings[1],file_settings[3]] = result
        return self.book
    
class MTEngine:
    def __init__(self) -> None:
        self.name = None

    def __repr__(self) -> str:
        return f"MTEngine(name={self.name})"

    def translate(self, text, source_language, target_language, **kwargs):
        ...

    def translate_batch(self, text_list:list, source_language, target_language, **kwargs):
        ...
        
    def support_languages(self):
        return None

class Tencent(MTEngine):
    def __init__(self, id=None, key=None, region=None) -> None:
        super().__init__()
        self.name = "Tencent"
        self.id = id
        self.key = key
        self.cred = credential.Credential(self.id, self.key)
        self.client = tmt_client.TmtClient(self.cred, region=region)

    def _translate(self, text, source_language='auto', target_language='zh', interval=1):
        params = {
            "SourceText": text,
            "Source": source_language,
            "Target": target_language,
            "ProjectId": 0,
        }
        req = models.TextTranslateRequest()
        req.from_json_string(json.dumps(params))
        resp = self.client.TextTranslate(req)
        time.sleep(interval)
        return resp.TargetText

    def _translate_batch(self, text_list:list, source_language='auto', target_language='zh', interval=1):
        params = {
            "SourceTextList": text_list,
            "Source": source_language,
            "Target": target_language,
            "ProjectId": 0,
        }
        req = models.TextTranslateBatchRequest()
        req.from_json_string(json.dumps(params))
        resp = self.client.TextTranslateBatch(req)
        time.sleep(interval)
        return resp.TargetTextList
    
    def split_text(self, text,limit=2000):
        result = []
        if len(text) > limit:
            while len(text) > limit:
                to_split = text[:limit]
                split_index = max(to_split.rfind("."), to_split.rfind("\n"), 1999)
                result.append(text[: split_index + 1])
                try:
                    text = text[split_index + 1 :]
                except IndexError:
                    text = ""
            result.append(text)
        else:
            result = [text]
        return result
    
    def translate(self, text, source_language='auto', target_language='zh', interval=1):
        text_list = self.split_text(text)
        trans_result = []
        for t in text_list:
            trans_result.append(self._translate(t,source_language, target_language, interval))
        # trans = pd.Series(trans_result).str.replace('{.+?/}',lambda x: x.group(0).replace(' ','').lower(),regex=True)
        translated = ''.join(trans_result)
        translated = re.sub('{.+?/}',lambda x: x.group(0).replace(' ','').lower(), translated)
        return translated
    
    def translate_batch(self, text_list: list, source_language='auto', target_language='zh', interval=1):
        translated = []
        if sum(map(len, text_list))>6000:
            for t in text_list:
                translated.append(self.translate(t,source_language,target_language,interval))
        else:
            translated = self._translate_batch(text_list,source_language,target_language,interval)
        trans = pd.Series(translated).str.replace('{.+?/}',lambda x: x.group(0).replace(' ','').lower(),regex=True)
        translated = trans.to_list()
        return translated
    
    def support_languages(self):
        langs = {
            "zh(简体中文)": [
                "en(英语)",
                "ja(日语)",
                "ko(韩语)",
                "fr(法语)",
                "es(西班牙语)",
                "it(意大利语)",
                "de(德语)",
                "tr(土耳其语)",
                "ru(俄语)",
                "pt(葡萄牙语)",
                "vi(越南语)",
                "id(印尼语)",
                "th(泰语)",
                "ms(马来语)",
            ],
            "zh-TW(繁体中文)": [
                "en(英语)",
                "ja(日语)",
                "ko(韩语)",
                "fr(法语)",
                "es(西班牙语)",
                "it(意大利语)",
                "de(德语)",
                "tr(土耳其语)",
                "ru(俄语)",
                "pt(葡萄牙语)",
                "vi(越南语)",
                "id(印尼语)",
                "th(泰语)",
                "ms(马来语)",
            ],
            "en(英语)": [
                "zh(中文)",
                "ja(日语)",
                "ko(韩语)",
                "fr(法语)",
                "es(西班牙语)",
                "it(意大利语)",
                "de(德语)",
                "tr(土耳其语)",
                "ru(俄语)",
                "pt(葡萄牙语)",
                "vi(越南语)",
                "id(印尼语)",
                "th(泰语)",
                "ms(马来语)",
                "ar(阿拉伯语)",
                "hi(印地语)",
            ],
            "ja(日语)": ["zh(中文)", "en(英语)", "ko(韩语)"],
            "ko(韩语)": ["zh(中文)", "en(英语)", "ja(日语)"],
            "fr(法语)": [
                "zh(中文)",
                "en(英语)",
                "es(西班牙语)",
                "it(意大利语)",
                "de(德语)",
                "tr(土耳其语)",
                "ru(俄语)",
                "pt(葡萄牙语)",
            ],
            "es(西班牙语)": [
                "zh(中文)",
                "en(英语)",
                "fr(法语)",
                "it(意大利语)",
                "de(德语)",
                "tr(土耳其语)",
                "ru(俄语)",
                "pt(葡萄牙语)",
            ],
            "it(意大利语)": [
                "zh(中文)",
                "en(英语)",
                "fr(法语)",
                "es(西班牙语)",
                "de(德语)",
                "tr(土耳其语)",
                "ru(俄语)",
                "pt(葡萄牙语)",
            ],
            "de(德语)": [
                "zh(中文)",
                "en(英语)",
                "fr(法语)",
                "es(西班牙语)",
                "it(意大利语)",
                "tr(土耳其语)",
                "ru(俄语)",
                "pt(葡萄牙语)",
            ],
            "tr(土耳其语)": [
                "zh(中文)",
                "en(英语)",
                "fr(法语)",
                "es(西班牙语)",
                "it(意大利语)",
                "de(德语)",
                "ru(俄语)",
                "pt(葡萄牙语)",
            ],
            "ru(俄语)": [
                "zh(中文)",
                "en(英语)",
                "fr(法语)",
                "es(西班牙语)",
                "it(意大利语)",
                "de(德语)",
                "tr(土耳其语)",
                "pt(葡萄牙语)",
            ],
            "pt(葡萄牙语)": [
                "zh(中文)",
                "en(英语)",
                "fr(法语)",
                "es(西班牙语)",
                "it(意大利语)",
                "de(德语)",
                "tr(土耳其语)",
                "ru(俄语)",
            ],
            "vi(越南语)": ["zh(中文)", "en(英语)"],
            "id(印尼语)": ["zh(中文)", "en(英语)"],
            "th(泰语)": ["zh(中文)", "en(英语)"],
            "ms(马来语)": ["zh(中文)", "en(英语)"],
            "ar(阿拉伯语)": ["en(英语)"],
            "hi(印地语)": ["en(英语)"],
        }
        return langs

class Deepl(MTEngine):
    def __init__(self, key=None) -> None:
        super().__init__()
        self.name = "Deepl"
        self.key = key

    def _translate(self, text, source_language, target_language, interval, batch=False):
        url = "https://api-free.deepl.com/v2/translate"
        headers = {"Authorization": self.key}
        payload = {
            "text": text,
            "target_lang": target_language,
            "source_lang": source_language,
        }
        response = requests.post(url, headers=headers, data=payload)
        if batch:
            result_text = [t['text'] for t in response.json()['translations']]
        else:
            try:
                result_text = response.json()["translations"][0]["text"]
            except:
                result_text = ""
        time.sleep(interval)
        return result_text

    def translate(self, text, source_language, target_language, interval):
        return self._translate(text, source_language, target_language, interval, False)

    def translate_batch(self, text_list: list, source_language, target_language, interval):
        return self._translate(text_list, source_language, target_language, interval, True)
    
    def support_languages(self):
        langs = {
            "source_lang": {
                "BG": "保加利亚语",
                "CS": "捷克语",
                "DA": "丹麦语",
                "DE": "德语",
                "EL": "希腊语",
                "EN": "英语",
                "ES": "西班牙语",
                "ET": "爱沙尼亚语",
                "FI": "芬兰语",
                "FR": "法语",
                "HU": "匈牙利语",
                "ID": "印尼语",
                "IT": "意大利语",
                "JA": "日语",
                "KO": "韩语",
                "LT": "立陶宛语",
                "LV": "拉脱维亚语",
                "NB": "挪威语（博克马尔语）",
                "NL": "荷兰语",
                "PL": "波兰语",
                "PT": "葡萄牙语（所有葡萄牙语变种混合）",
                "RO": "罗马尼亚语",
                "RU": "俄语",
                "SK": "斯洛伐克语",
                "SL": "斯洛文尼亚语",
                "SV": "瑞典语",
                "TR": "土耳其语",
                "UK": "乌克兰语",
                "ZH": "中文",
            },
            "target_lang": {
                "BG": "保加利亚语",
                "CS": "捷克语",
                "DA": "丹麦语",
                "DE": "德语",
                "EL": "希腊语",
                "EN": "英语（未指定变种，为了向后兼容，请选择英国英语或美国英语）",
                "EN-GB": "英语（英国）",
                "EN-US": "英语（美国）",
                "ES": "西班牙语",
                "ET": "爱沙尼亚语",
                "FI": "芬兰语",
                "FR": "法语",
                "HU": "匈牙利语",
                "ID": "印尼语",
                "IT": "意大利语",
                "JA": "日语",
                "KO": "韩语",
                "LT": "立陶宛语",
                "LV": "拉脱维亚语",
                "NB": "挪威语（博克马尔语）",
                "NL": "荷兰语",
                "PL": "波兰语",
                "PT": "葡萄牙语（未指定变种，为了向后兼容，请选择巴西葡萄牙语或葡萄牙葡萄牙语）",
                "PT-BR": "葡萄牙语（巴西）",
                "PT-PT": "葡萄牙语（除巴西葡萄牙语之外的所有葡萄牙语变种）",
                "RO": "罗马尼亚语",
                "RU": "俄语",
                "SK": "斯洛伐克语",
                "SL": "斯洛文尼亚语",
                "SV": "瑞典语",
                "TR": "土耳其语",
                "UK": "乌克兰语",
                "ZH": "中文（简体）",
            },
        }
        return langs

class Google(MTEngine):
    def __init__(self) -> None:
        super().__init__()
        self.name = "Google"

    def translate(self, text, source_language='auto', target_language='zh-CN', interval=1):
        translator = GoogleTranslator(source_language,target_language)
        result = translator.translate(text)
        time.sleep(interval)
        return result

    def translate_batch(self, text_list: list, source_language='auto', target_language='zh-CN', interval=1):
        results=[]
        for t in text_list:
            results.append(self.translate(t,source_language, target_language, interval))
        return results

    def support_languages(self):
        return GoogleTranslator().get_supported_languages(True)
