# AILANG v0.12.0 Benchmarks — AI writes a new language better than Python

**Status:** skeleton — fill with prose
**Target length:** 1500–2500 words
**Publishing slot:** standalone (not part of the trust series — publish when timely, e.g. after a new model release)
**Author tag:** `me`
**Tags:** `ailang`, `benchmarks`, `ai-coding`, `programming-languages`
**Hero visual:** [programming-language-performance-heatmap.png](/Users/mark/dev/sunholo/ailang/docs/static/img/programming-language-performance-heatmap.png)
**Slug:** `/ailang-benchmarks-v0120`

---

## 1. Hook — the counterintuitive finding (~200 words)

AILANG is a new language. It isn't in GPT's training data. It isn't in Claude's. No model has seen it before. And yet, across 612 benchmark runs on v0.12.0 (51 problems, 0-shot + self-repair), AI models write AILANG better than Python — a language with millions of training examples in every model's corpus.

The finding is counterintuitive: shouldn't a model with zero training examples in a language perform *worse* than in the language it's seen millions of times? The answer tells us something important about what AI models actually learn when they learn to code — and about what kind of language structure helps or hinders them.

---

## 2. The eval setup (~200 words)

Describe the benchmark methodology:

- 51 problems ranging from easy to hard
- Two eval modes:
  - **Standard eval:** 0-shot generation with one self-repair attempt. Model sees the problem, writes code, gets test feedback, gets one chance to fix.
  - **Agent eval:** multi-turn CLI execution with iterative feedback. Model can run code, read errors, and iterate.
- Each problem tested in both AILANG and Python
- 6 models for standard eval, 2 agent executors for agent eval
- Eval environment runs Python 3.9.5 (relevant — models sometimes try Python 3.10+ syntax and fail)
- All runs are 0-shot: no few-shot examples, no AILANG documentation in the prompt. The model must infer the language from the problem specification alone.

---

## 3. The results (~400 words)

### Standard eval — single-shot with one self-repair attempt

| Rank | Model | AILANG | Python | Delta | Cost | Tokens |
|---|---|---|---|---|---|---|
| 1 | Claude Opus 4.7 | 86.3% | 82.4% | +~4 pp | $9.10 | 1.67M |
| 1 | GPT-5.4 | 86.3% | 82.4% | +~4 pp | $3.04 | 1.11M |
| 3 | Claude Sonnet 4.6 | 86.3% | 80.4% | +~6 pp | $4.21 | 1.44M |
| 4 | Gemini 3.1 Pro | 82.4% | 78.4% | +~4 pp | $2.60 | 1.33M |
| 5 | GPT-5.2 Codex | 76.5% | 80.4% | -~4 pp | $2.27 | 1.10M |
| 6 | Gemini 3 Flash | 82.4% | 70.6% | +~12 pp | $0.66 | 1.28M |

Prose analysis — things to notice:

1. **Structure helps across the board.** AILANG ≥ Python for 4 of 6 models. The biggest advantage — +~12 pp — belongs to the cheapest model. Structure doesn't just help the best; it helps the most constrained the most.

2. **Cost matters.** GPT-5.4 matches Opus for a third of the price. Gemini Flash gets 82.4% for sixty-six cents. The "best model wins" framing is incomplete without the cost column — and the cost column favours structured languages because they need fewer tokens to converge.

3. **GPT-5.2 Codex is the exception.** The only model where Python wins. Worth investigating: is this a Codex-specific training signal, or noise at this sample size?

### Agent eval — multi-turn with CLI execution

| Executor | AILANG | Python | Avg turns | Avg cost/run |
|---|---|---|---|---|
| Claude Code (Sonnet 4.5) | 97.7% | 97.7% | 4.3 | $0.073 |
| Gemini CLI (Gemini 3 Flash) | 39.1% | 43.5% | — | — |

The agent-eval headline: Claude Code with iterative feedback near-perfects both languages — the multi-turn loop closes the gap that 0-shot leaves open. Structure is learnable, not a barrier.

**Iterative feedback is a great equaliser.** In agent mode, a model that scores 86% in 0-shot can reach 97.7% with a few repair turns. This is the same pattern as human code review — the first draft isn't the point; the feedback loop is.

---

## 4. A concrete example: the mini interpreter (~400 words)

One of the 51 benchmarks asks models to build an interpreter for a mini-language — define an AST with five node types (numeric literals, variables, addition, multiplication, let-bindings), implement an evaluator, and run a nested expression. It is rated "hard." Both AILANG and Python pass 6 of 6 models. The difference is in the code.

### AILANG (Claude Opus 4.7)

```typescript
// AILANG
type Expr = Num(int) | Var(string) | Add(Expr, Expr) 
          | Mul(Expr, Expr) | Let(string, Expr, Expr)

func lookup(name: string, env: [(string, int)]) -> int =
  match env {
    [] => 0,
    pair :: rest => match pair {
      (n, v) => if n == name then v else lookup(name, rest)
    }
  }

func eval(expr: Expr, env: [(string, int)]) -> int =
  match expr {
    Num(n) => n,
    Var(x) => lookup(x, env),
    Add(a, b) => eval(a, env) + eval(b, env),
    Mul(a, b) => eval(a, env) * eval(b, env),
    Let(name, e1, e2) => {
      let v = eval(e1, env);
      eval(e2, (name, v) :: env)
    }
  }
```

### Python (same model, same task)

```python
@dataclass
class Num:
    value: int

@dataclass
class Var:
    name: str

@dataclass
class Add:
    left: 'Expr'
    right: 'Expr'

@dataclass
class Mul:
    left: 'Expr'
    right: 'Expr'

@dataclass
class Let:
    name: str
    value: 'Expr'
    body: 'Expr'

Expr = Union[Num, Var, Add, Mul, Let]

def eval(expr: Expr, env: Env) -> int:
    if isinstance(expr, Num):
        return expr.value
    if isinstance(expr, Var):
        return lookup(expr.name, env)
    if isinstance(expr, Add):
        return eval(expr.left, env) + eval(expr.right, env)
    if isinstance(expr, Mul):
        return eval(expr.left, env) * eval(expr.right, env)
    if isinstance(expr, Let):
        val = eval(expr.value, env)
        return eval(expr.body, [(expr.name, val)] + env)
    raise TypeError(f"Unknown expression: {expr}")
```

### What the code tells us

Both work. Both pass 6 of 6 models. Look at the structural difference.

In AILANG, the entire AST — five node types with their fields — is a single line. The `eval` function uses pattern matching that the compiler verifies is exhaustive: miss a case and the code won't build. The structure tells the AI exactly what shape the solution must take.

In Python, the same AST requires five separate class definitions and a `Union` type alias. The evaluator is an `isinstance` chain — and the `raise TypeError` at the bottom exists only because the type system *can't guarantee* you covered every case. It's a runtime safety net for a problem that AILANG solves at compile time.

No model has seen AILANG in its training data. Every model has seen millions of lines of Python. And yet the AI produces cleaner code in the language it has never seen — because the language's structure guides it to the right answer.

---

## 5. More examples (~300 words)

Include 2-3 additional benchmark examples that illustrate different aspects of the AILANG advantage:

### Example: Record update syntax
- AILANG 6/6, Python 2/6
- Python failures are `IMPERATIVE` errors — `True` vs `true` capitalisation
- Shows how Python's conventions (capitalised booleans) trip up models, while AILANG's consistent lowercase avoids the issue

### Example: State machine (elevator)
- Include the elevator benchmark if it shows an interesting structural comparison
- ADT + exhaustive match vs class hierarchy + if/elif chains

### Example: [find one where AILANG wins cleanly without WRONG_LANG confound]
- Look in eval results for benchmarks where AILANG passes and Python fails for structural reasons, not runtime version issues

---

## 6. Why does this happen? (~300 words)

The explanation section. Why does a zero-training-data language outperform a mature one?

Three hypotheses (present as complementary, not competing):

1. **Algebraic data types compress the solution space.** A single-line ADT tells the model the exact shape of the data. Five dataclasses scatter the same information across 20 lines. Compression reduces the chance of omission.

2. **Exhaustive matching eliminates a class of errors.** The compiler catches missing cases. In Python, a missing `isinstance` branch is a silent bug that only surfaces at runtime — if the test happens to hit that branch.

3. **One canonical form reduces ambiguity.** Python has multiple ways to express the same pattern (dataclass vs namedtuple vs dict vs class). Each model picks differently, and not all choices compose well. AILANG has one way, and the model finds it.

The general principle: **constraint is not the opposite of capability. It is how you get reliable capability.** This is the same argument as the trust series — applied to language design rather than delegation architecture.

---

## 7. What this means for AI-assisted development (~200 words)

The so-what section.

- Language design is AI infrastructure now. The language your AI writes in affects its error rate, cost, and auditability.
- "Just use Python" is a default, not a decision. The benchmarks suggest it's not always the best one.
- Structure is learnable. The agent eval shows that with feedback loops, models converge on AILANG just as well as Python. The barrier to adoption is human familiarity, not AI capability.
- Forward pointer: AILANG benchmarks will be updated with each new model release. Subscribe for the next round.

---

## Cutting-room floor — do NOT include

- AILANG product pitch or roadmap — this is a benchmarks analysis post, not a launch
- Detailed eval methodology paper (save for a docs page)
- Comparison to languages other than Python (Go, Rust, etc.) — not yet benchmarked
- Effect system, capability declarations, entropy budgets — save for the trust series
- Claims about production readiness — AILANG is in research/beta

## Editorial notes

- First-person, Mark voice
- The tables are the shareable artefact — design them for screenshot
- Lead with the counterintuitive finding, not the language pitch
- Link back to the trust series if published: "I explored the *why* — why structure helps — in my series on AI trust and authority"
- Benchmark posts perform well when new models come out — keep the template reusable for v0.13.0, v0.14.0 etc.
- Python 3.9 vs 3.10 issue: mention it honestly in the methodology section. Some Python failures are `WRONG_LANG` (model tries `match/case` on 3.9). This is itself an interesting data point — models default to newer syntax they've seen more of in training.
