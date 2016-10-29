# Skippity

Python skiplist implementation with fast median discovery. Ideal for rolling median problems such as this: [Hackerrank median](https://www.hackerrank.com/challenges/median).

## Debug
comes with neat debug visualization
```
    ______  2 ___________  5 ______  7 _
    _  1 _  2 _  3 ______  5 ______  7 _
    _  1 _  2 _  3 _  4 _  5 _  6 _  7 _
```

For median discovery, each node knows how much base nodes will going forward in the current layer skip

```
  1 ______  2 ___________  1 ______  0 _
  0 _  0 _  0 _  1 ______  1 ______  0 _
  0 _  0 _  0 _  0 _  0 _  0 _  0 _  0 _
```