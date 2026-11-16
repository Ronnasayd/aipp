---
description: Start an interactive quiz pane (quiz-mod) — ask the user for topic and number of questions, then generate the quiz
disable-model-invocation: true
---

Start a quiz using the `quiz-mod` plugin.

1. Use `AskUserQuestion` to ask the user:
   - What topic the quiz should cover (e.g. "this repo overall", "a specific file/dir", "general knowledge", or a free-text topic).
   - How many questions (offer a few sensible defaults, e.g. 3 / 5 / 8).
2. If the topic is about the repo as a whole, cover all its relevant/main parts, not just architecture — mix in things like core modules/components, configuration, dependencies/integrations, build/test/deploy setup, and any other main pieces specific to this project, as fits the question count. If the topic is a specific file/dir, scope to that. Read the relevant files first (use rag-rat / Grep / Read) so the questions are grounded in real code, not guesses.
3. Write that many multiple-choice questions (3-4 options each, one correct) on the chosen topic.
4. Call `mcp__quiz-mod__quiz_start` with the `questions` array.
5. Tell the user the quiz pane is open and they should answer it there.
6. When the user says they're done, call `mcp__quiz-mod__quiz_result` and report the score and any wrong answers.
