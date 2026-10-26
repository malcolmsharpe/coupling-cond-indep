---
title: "Non-uniqueness of maximal recoupling: example"
date: 2024-10-07T20:42:40+00:00
modified: 2024-10-07T20:42:40+00:00
url: https://masharpe.wordpress.com/2024/10/07/non-uniqueness-of-maximal-recoupling-example/
tags: ["coupling", "example", "research"]
categories: ["Uncategorized"]
---

# Non-uniqueness of maximal recoupling: example

Classic maximal couplings are well-known to be non-unique in general. Maximal recoupling however imposes more constraints than maximal coupling–are those constraints enough to force uniqueness? In fact they aren’t, as we’ll show here with a simple example.

Let the initial joint distribution be:

```
X,Y =
    a,c wp 1/4
    b,c wp 1/4
    c,d wp 1/4
    c,e wp 1/4
```

so the marginals are

```
X =
    a wp 1/4
    b wp 1/4
    c wp 1/2

Y =
    c wp 1/2
    d wp 1/4
    e wp 1/4
```

In graph form, a and b are sources, d and e are sources, and c is neither:

```
a     d
 \   ^
  v /
   c
  ^ \
 /   v
b     e
```

It’s easy to find two different decompositions of this flow into a distribution of walks, which, by shortcutting each walk, yield distinct MRCs:

```
#1
X,Y =
    c,c wp 1/2
    a,d wp 1/4
    b,e wp 1/4

#2
X,Y =
    c,c wp 1/2
    a,e wp 1/4
    b,d wp 1/4
```

Verifying that there are indeed MRCs will wait for the future, since I have not nailed down the ideal definition for “a maximal recoupling”. But any reasonable definition should find that these are both MRCs.
