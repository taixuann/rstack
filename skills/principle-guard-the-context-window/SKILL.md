---
name: principle-guard-the-context-window
description: "Apply when context fills with large data, long papers, or repeated reads. Route bulk reading to workers and keep summaries in the main thread."
disable-model-invocation: true
---

# Guard The Context Window

Do not paste raw data or full papers into the main thread. Send bulk reading and per-slice processing to workers with a self-contained brief, and take back a short report with a path to the full output. Read files in ranges, summarize, and note where the detail lives.
