---
title: "Pitfalls of binary-outcome matches for LLM evaluation"
date: 2024-05-04T15:13:44+00:00
modified: 2024-05-04T15:13:44+00:00
url: https://masharpe.wordpress.com/2024/05/04/pitfalls-of-binary-outcome-matches-for-llm-evaluation/
tags: ["coupling", "evaluation", "llm"]
categories: ["Uncategorized"]
---

# Pitfalls of binary-outcome matches for LLM evaluation

Let’s say we have two LLMs and we want to determine which we prefer. One of the most effective approaches in practice is the one used by the lmsys chatbot arena: feed a single prompt to both LLMs, show the responses blinded to the user, and ask which one the user prefers. This is done many times, and then the win-loss data is analyzed with a rating model (such as the Bradley-Terry model, which is related to Elo).

However, this method, of using matches with binary outcomes, has some strange properties, discussed below.

## Non-transitivity is possible

The usual non-transitive dice examples apply, so there can be models A B C such that A>B>C>A, where “>” means a winrate above 50%.

## Coupling can change the ranking

In previous posts, I’ve discussed coupling, which introduces a dependence between the two responses to make them easier to compare. But, unfortunately, when using matches with binary outcomes, coupling can change the ranking compared to uncoupled models.

Example: Consider a model A that has utilities 1,3,5 and a model B with utilities 2,4,6. Uncoupled, you obviously have B>A. But we can couple to make A win instead:

- 1<6
- 3>2
- 5>4

With this coupling, A wins 67% of matches!

## A bad model can outrank a good model

Consider a model A that is perfectly consistent with utility 9 and a model B that is 60% utility 10 and 40% utility 0. Then B>A by winrate, but, for downstream tasks, you’d probably prefer A.

I suspect that this might happen in practice. A might be a smart model and B a dumb model fine-tuned with a nice writing style. B will fail utterly on hard problems, but it’ll give slightly nicer answers on easy problems, so as long as there are enough easy problems in the pool, B will have a favorable winrate vs A. Though I don’t have evidence, I suspect this might explain occasional cases of small models ranking surprisingly high on the chatbot arena leaderboard.

## A tentative alternative

In principle, each model’s responses have a distribution of utility, and you’d like to rank models according to their expected utility. To implement this using pairwise comparisons, you’d have human evaluators specify the difference in utility between the two answers. That scheme eliminates all the previously discussed problems.

It’s not clear though how to make this into a practical system. Giving a numerical difference in utility is likely to be hard for any one evaluator and inconsistent between evaluators. Even an intermediate solution, such as allowing expressing strength of preference (e.g. strongly A, weakly A, tie, weakly B, strongly B), starts to have those problems.

In any case, if you *can* give feedback that’s the utility difference between two responses, then coupling is useful as variance reduction, since it allows a matched pairs experimental design.
