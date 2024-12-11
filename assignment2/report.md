--report! --

- Moving from OOP to functional changed how I approached the program's structure. Objects managing their own analysis state had to be replaced with a complete separation of data and behavior. The design shifted from organizing individual analyzers to planning a series of data transformations.

- State tracking became explicit through function parameters instead of living in instance variables, which simplified tracking indentation and class context across the codebase.

I followed functional principles by:

Using immutable data structures (frozenset) to prevent state changes
Writing pure functions that only depend on their inputs
Building a pipeline of data transformations
Isolating file I/O to the program edges

The code became more predictable since functions operate only on their inputs without hidden state affecting the outputs.