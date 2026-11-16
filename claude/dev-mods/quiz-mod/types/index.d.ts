export type QuizQuestion = {
  question: string;
  options: string[];
  correctIndex: number;
};

export type QuizAnswer = {
  questionIndex: number;
  chosenIndex: number;
  correct: boolean;
};

export type QuizState = {
  questions: QuizQuestion[];
  current: number;
  answers: QuizAnswer[];
  done: boolean;
};

declare module "claude-code" {
  interface PluginState {
    "quiz-mod": { quiz: Shaped<QuizState> };
  }
}
