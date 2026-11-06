---
model: sonnet
description: Turn a rough request into a clear, complete prompt ready to paste
argument-hint: <rough prompt or idea>
disable-model-invocation: true
---

Turn the user's rough input below into a good prompt. Do not carry out the task it describes: your only deliverable is the prompt.

<user_input>
$ARGUMENTS
</user_input>

If the input is empty, ask the user what they want the prompt to achieve, then continue.

## 1. Check the input against these elements

| Element     | Question it answers                                                |
| ----------- | ------------------------------------------------------------------ |
| Objective   | What concrete result is expected? A result, not a topic.           |
| Reason      | Why does it matter? This guides decisions in cases nobody foresaw. |
| Context     | Which files, exact errors, stack and past attempts are relevant?   |
| Constraints | What must not change (libraries, public API, scope)?               |
| Done when   | What verifiable criterion shows success?                           |
| Output      | What format and length should the answer have?                     |

## 2. Fill the gaps

- If the input names code, files or errors, read them and fill Context with real paths and exact messages. Never invent paths, errors or requirements.
- Ask with `AskUserQuestion` only about gaps that would change the result, in one round of at most 4 questions. Explain in each question why the answer matters, and offer concrete options.
- Omit an element that does not apply to the task rather than padding it.

## 3. Write the prompt

Use this structure, in the same language as the user's input:

```text
Objective: <expected result>
Reason: <why it matters>
Context: <files, errors, what was tried>
Constraints: <what must not change>
Done when: <verifiable criterion>
Output: <format>
```

Apply these only where they help:

- Add 1-3 input/output examples when the expected format is hard to describe.
- Wrap pasted data in XML tags or code blocks, so it stays separate from the instructions.
- State instructions positively: "answer in 3 sentences", not "don't be verbose".
- Add "if information is missing, say so" when the task depends on facts that could be guessed.
- Split work that is too big for one prompt into ordered steps (plan, review, execute).
- Keep only relevant context, because noise degrades the result.

## 4. Check before answering

A colleague with no context must be able to execute the prompt without asking anything. If they could not, fix it or ask the user.

## 5. Answer

Show the final prompt in a single code block, followed by at most 3 short lines on what you added or assumed. Mark any remaining unknown as `<fill in: ...>` inside the prompt.
