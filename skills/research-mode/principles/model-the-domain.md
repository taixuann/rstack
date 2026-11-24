---
name: principle-model-the-domain
description: "Apply before writing analysis code. Name the data shape first: units, dimensions, sampling, subject and session structure, and the schema of every table."
disable-model-invocation: true
---

# Model The Domain

Write down what one row is, what each column means with its unit, how subjects, sessions, and channels nest, and what the primary key is. Encode it as a schema or typed loader. Many analysis errors are shape errors: pseudoreplication, wrong grouping, mixed units.
