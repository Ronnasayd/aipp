import { atom, read, update } from "claude-code";
import type { Register } from "claude-code";

import type { QuizQuestion, QuizState } from "../types";

const PANE = "quiz";
const EMPTY: QuizState = {
  questions: [],
  current: 0,
  answers: [],
  done: false
};
// why: shape tag bumps when QuizState's fields change, so the engine declines
// what an earlier version stored instead of handing back a stale shape.
const quiz = atom({ plugin: "quiz-mod", key: "quiz" } as const, EMPTY, {
  shape: "quiz-1"
});

function score(state: QuizState) {
  const correct = state.answers.filter((a) => a.correct).length;
  return { correct, total: state.questions.length };
}

export const register: Register = (on) => {
  on("session.start", async ($, e, next) => {
    await $.tool.register({
      name: "quiz_start",
      description:
        "Open a quiz pane with the given questions and let the user answer them one at a time by clicking an option. Call quiz_result afterwards to read the score.",
      inputSchema: {
        type: "object",
        properties: {
          questions: {
            type: "array",
            items: {
              type: "object",
              properties: {
                question: { type: "string" },
                options: { type: "array", items: { type: "string" } },
                correctIndex: { type: "number" }
              },
              required: ["question", "options", "correctIndex"]
            }
          }
        },
        required: ["questions"]
      }
    });

    await $.tool.register({
      name: "quiz_result",
      description:
        "Read the current quiz score and the list of wrong answers (with the correct option) once the user has finished answering."
    });

    return next(e);
  });

  on("tool.call", { tool: "mcp__quiz-mod__quiz_start" }, async ($, e) => {
    const questions = (e as unknown as { questions: QuizQuestion[] }).questions;
    await update($, quiz, () => ({
      questions,
      current: 0,
      answers: [],
      done: questions.length === 0
    }));
    await $.ui.open({ id: PANE, title: "Quiz" });

    return { result: `Quiz pane opened with ${questions.length} questions.` };
  });

  on("tool.call", { tool: "mcp__quiz-mod__quiz_result" }, async ($) => {
    const state = await read($, quiz);

    if (!state.done) {
      return {
        result: `Quiz still in progress: ${state.answers.length}/${state.questions.length} answered.`
      };
    }

    const { correct, total } = score(state);
    const wrong = state.answers
      .filter((a) => !a.correct)
      .map((a) => {
        const q = state.questions[a.questionIndex]!;
        return `- "${q.question}" — you picked "${q.options[a.chosenIndex]}", correct was "${q.options[q.correctIndex]}"`;
      })
      .join("\n");

    return {
      result: `Score: ${correct}/${total}.${wrong ? `\nWrong answers:\n${wrong}` : ""}`
    };
  });

  on("ui.render", { component: "Pane", requestId: PANE }, async ($, e) => {
    const { Box, Text, Button } = $.ui.resolve(e);
    const state = await read($, quiz);

    if (state.questions.length === 0) {
      return (
        <Box
          flexDirection="column"
          borderStyle="round"
          borderColor="subtle"
          paddingX={1}
        >
          <Text dimColor>No quiz loaded yet.</Text>
        </Box>
      );
    }

    if (state.done) {
      const { correct, total } = score(state);
      const wrong = state.answers.filter((a) => !a.correct);
      const allCorrect = wrong.length === 0;

      return (
        <Box flexDirection="column" gap={1}>
          <Box
            flexDirection="row"
            gap={1}
            borderStyle="round"
            borderColor={allCorrect ? "green" : "yellow"}
            paddingX={1}
          >
            <Text bold color={allCorrect ? "green" : "yellow"}>
              Score: {correct}/{total}
            </Text>
          </Box>
          {allCorrect && <Text dimColor>No mistakes.</Text>}
          {wrong.map((a) => {
            const q = state.questions[a.questionIndex]!;
            return (
              <Box
                key={`wrong-${a.questionIndex}`}
                flexDirection="column"
                borderStyle="round"
                borderColor="danger"
                paddingX={1}
              >
                <Text bold>{q.question}</Text>
                <Text color="danger">you: {q.options[a.chosenIndex]}</Text>
                <Text color="green">correct: {q.options[q.correctIndex]}</Text>
              </Box>
            );
          })}
        </Box>
      );
    }

    const q = state.questions[state.current]!;

    return (
      <Box flexDirection="column" gap={1}>
        <Box
          flexDirection="column"
          borderStyle="round"
          borderColor="claude"
          paddingX={1}
        >
          <Text bold dimColor>
            Question {state.current + 1}/{state.questions.length}
          </Text>
          <Text bold>{q.question}</Text>
        </Box>
        <Box flexDirection="column" gap={1}>
          {q.options.map((option, index) => (
            <Button
              key={`opt-${index}`}
              label={option}
              onPress={async () => {
                const current = await read($, quiz);
                const answer = {
                  questionIndex: current.current,
                  chosenIndex: index,
                  correct:
                    index === current.questions[current.current]!.correctIndex
                };
                const next = current.current + 1;
                await update($, quiz, (s) => ({
                  ...s,
                  current: next,
                  answers: [...s.answers, answer],
                  done: next >= s.questions.length
                }));
              }}
            />
          ))}
        </Box>
      </Box>
    );
  });
};
