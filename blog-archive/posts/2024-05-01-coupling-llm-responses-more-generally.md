---
title: "Coupling LLM responses more generally"
date: 2024-05-01T22:43:47+00:00
modified: 2024-05-01T22:45:04+00:00
url: https://masharpe.wordpress.com/2024/05/01/coupling-llm-responses-more-generally/
tags: ["coupling", "llm", "research", "sampling"]
categories: ["Uncategorized"]
---

# Coupling LLM responses more generally

Suppose you want to compare nondeterministic responses from two LLMs with the aim of picking your preferred model. The simplest option is to generate a response from each and compare them. That works, but the responses might be very different, making it challenging to weigh all the differences; also, the worse model might beat the better model by luck.

To help with those two problems, we’d like to make the responses more similar by coupling them. In a previous post, I presented the APOC algorithm to do this, but APOC has limitations:

- It must be possible to do forward passes with each model. Black box APIs typically do not allow this.
- The criterion for response similarity is implicitly the length of the shared prefix. You might prefer a different criterion.
- APOC is difficult to implement when the models have different tokenizers.

Here’s a more general strategy for coupling, which requires only the ability to generate responses:

- For some chosen `n`, generate `n` responses from the LLMs A and B.
- For each A response and B response, compute their dissimilarity using your desired criterion.
- Pair the A responses and B responses, minimizing total dissimilarity via minimum-cost bipartite matching.
- Select a pair uniformly randomly and present it to the user. (Optionally, you may select more than one pair.)

Since the final choice is uniformly random, the responses seen are unbiased samples from the models.

Here are some examples of dissimilarity criteria to consider:

- Edit distance
- Absolute difference of length
- (In cases where the response is expected to contain a final answer, such as a math problem:) Whether the final answers differ

Note that the dissimilarity criterion calculation can use an LLM itself.
