---
title: "Which proprietary LLM API providers support seed for reproducibility"
date: 2024-08-20T02:50:34+00:00
modified: 2024-08-20T02:50:34+00:00
url: https://masharpe.wordpress.com/2024/08/20/which-proprietary-llm-api-providers-support-seed-for-reproducibility/
tags: ["llm", "market"]
categories: ["Uncategorized"]
archive_note: related post not in the author's core list
---

# Which proprietary LLM API providers support seed for reproducibility

For uses such as evaluation, it can be useful to get reproducible outputs from an LLM. When generating with a non-zero temperature, one must specify a seed to achieve reproducible outputs. This is always an option when self-hosting an open LLM, but, for proprietary LLMs, some providers don’t offer a seed parameter. (My interest is that APOC improves the coupling obtained by using a shared seed, which makes APOC mainly appealing to users already using seeds.)

This post lists which proprietary LLM API providers support specifying a seed for generation. I produced this list by searching their documentation, so oversights are possible. Also, I have not tried using most of these APIs, which leaves open the question of whether the seed parameter is effective. (For example, OpenAI’s seed parameter is well-known to not ensure fully deterministic outputs.)

- OpenAI: [supported](https://platform.openai.com/docs/advanced-usage/reproducible-outputs)
- Google Gemini: not supported
- Anthropic: not supported
- Mistral: [supported](https://docs.mistral.ai/api/#tag/chat/operation/chat_completion_v1_chat_completions_post)
- 01.AI: not supported
- Reka: [supported](https://docs.reka.ai/api-reference/chat/create#request.body.seed)
- DeepSeek: not supported
- Cohere: [supported](https://docs.cohere.com/docs/predictable-outputs#seed)
- Qwen: [supported](https://www.alibabacloud.com/help/en/model-studio/developer-reference/use-qwen-by-calling-api#f7cf331c06b49)
