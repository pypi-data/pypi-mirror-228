# 🦜️🔗✨ LangChain-xfyun

⚡ 在LangChain中流畅地使用讯飞星火大模型 ⚡

[![Release Notes](https://img.shields.io/github/release/vsxd/langchain-xfyun)](https://github.com/vsxd/langchain-xfyun/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Open in Dev Containers](https://img.shields.io/static/v1?label=Dev%20Containers&message=Open&color=blue&logo=visualstudiocode)](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/vsxd/langchain-xfyun)
[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/vsxd/langchain-xfyun)
[![GitHub star chart](https://img.shields.io/github/stars/vsxd/langchain-xfyun?style=social)](https://star-history.com/#vsxd/langchain-xfyun)
[![Open Issues](https://img.shields.io/github/issues-raw/vsxd/langchain-xfyun)](https://github.com/vsxd/langchain-xfyun/issues)


## ⏩ 快速安装

`pip install langchain-xfyun`

## 🤔 这是什么？

大型语言模型（LLM）正在成为一种变革性技术，它使开发人员能够构建以前无法构建的应用程序。然而，孤立地使用这些 LLM 通常不足以创建真正强大的应用程序，只有将它们与其他计算或知识来源相结合，才能发挥真正的威力。

- Fork from [langchain](https://github.com/langchain-ai/langchain)

- 添加了讯飞星火大模型的支持，让你可以在langchain中使用SparkLLM

- [TODO] 修改langchain内置prompt以适应SparkLLM

- 其它关于langchain的信息可以参考 [LangChain's original README.md](https://github.com/vsxd/langchain-xfyun/blob/master/README-langchain.md)

## ❓ 如何使用

```python
from langchain_xfyun.chat_models import ChatSpark
from langchain_xfyun.prompts import ChatPromptTemplate
from langchain_xfyun.chains import LLMChain

llm = ChatSpark(app_id="your_app_id", api_key="your_api_key",
                api_secret="your_api_secret")

prompt = ChatPromptTemplate.from_template(
    "我有一个生产[{product}]商品的公司，请帮我取一个最合适的公司名称。只输出答案本身"
)

chain = LLMChain(llm=llm, prompt=prompt, verbose=True)

product = "魔方"
ans = chain.run(product)
print(ans)
```

- 像以前一样使用chat model，现在你可以使用`ChatSpark`而不是`ChatOpenAI`

- 更详细的内容请参考[langchain 官方文档](https://python.langchain.com/docs/use_cases/question_answering/)

## 💁 Contributing

As an open-source project in a rapidly developing field, we are extremely open to contributions, whether it be in the form of a new feature, improved infrastructure, or better documentation.

For detailed information on how to contribute, see [here](.github/CONTRIBUTING.md).
