---
title: "AILANG Cloud: Serverless AI Agent Orchestration for ~$60/month"
authors: solaris
tags: [product-launch, ailang-cloud, ailang]
slug: /ailang-cloud
image: ./img/ailang-cloud.webp
draft: true
---

![](./img/ailang-cloud.webp)

Today we're launching **AILANG Cloud** — a serverless execution platform that runs autonomous AILANG agent workflows on Google Cloud. Three components, five Pub/Sub topics, Terraform-managed infrastructure, and a full observability dashboard. Production cost: roughly $60/month.

<!-- truncate -->

:::info[AI-Generated Content]
This product announcement was written by Solaris, Sunholo's AI communications assistant, and reviewed by the Sunholo team.
:::

## Running AI agents locally doesn't scale

If you've built agent workflows with AILANG, you know the pattern: a coordinator dispatches tasks, agents execute them, results flow back. On your laptop, that works. But when you need agents running 24/7, handling GitHub webhooks, and surviving restarts — local execution hits a wall.

AILANG Cloud moves the entire coordinator stack to Google Cloud Run with Pub/Sub messaging. You push to a branch, Cloud Build deploys everything, and your agents run autonomously in ephemeral containers. No servers to manage, no processes to babysit.

## How it works

AILANG Cloud has three components, each running as a separate Cloud Run resource:

**Coordinator (Cloud Run Service).** The brain. It receives messages via Pub/Sub, maintains workflow state in Firestore, and dispatches agent tasks via the Cloud Run Jobs API. In dev, it scales to zero. In production, it stays warm with one vCPU always on.

**Agent Executor (Cloud Run Job).** The hands. Each task spawns an ephemeral container with Claude CLI, Gemini CLI, and git pre-installed. The agent does its work — writes code, creates PRs, runs tests — then exits. No long-running processes, no idle compute.

**Dashboard (Cloud Run Service).** The eyes. A React frontend backed by a Go server on port 1957. It receives OpenTelemetry traces, logs, and metrics at `/v1/traces`, giving you real-time visibility into every agent execution.

These three components communicate through **five Pub/Sub topics**: messages, tasks, completions, events, and a dead-letter topic for failed deliveries. Firestore serves as the source of truth for task state, message history, and workflow chains.

:::tip[Why Cloud Run Jobs instead of Eventarc?]
We chose the Cloud Run Jobs API over Eventarc for agent dispatch. It gives us better control over execution timing and lets us inject per-execution environment variables — critical when each agent task needs different context.
:::

## Three environments, one Terraform config

AILANG Cloud uses a single Terraform codebase with per-environment variable files. Each environment gets its own GCP project, its own state prefix, and its own scaling configuration:

| Environment | Project | Scaling | Use Case |
|-------------|---------|---------|----------|
| **dev** | `ailang-multivac-dev` | Scale-to-zero | Development, testing |
| **test** | `ailang-multivac-test` | Coordinator always-on | Integration testing |
| **prod** | `ailang-multivac` | All services always-on | Production workloads |

Deploy any environment with two commands:

```bash
cd terraform
terraform apply -var-file="environments/dev/terraform.tfvars"
```

CI/CD is automatic. Push to `dev`, `test`, or `prod` and Cloud Build triggers handle the rest — building images, running Terraform, and deploying services.

## Full observability with dual trace export

Every agent execution is traced end-to-end. AILANG Cloud exports OpenTelemetry data to two destinations simultaneously:

1. **The Dashboard** — traces, logs, and metrics arrive at the built-in observatory for real-time monitoring
2. **Google Cloud Trace** — the same data goes to GCP's native tracing for long-term analysis and alerting

You can watch an agent workflow execute in real time: coordinator receives a GitHub webhook, dispatches a design-doc agent, which completes and triggers a sprint-planner, which dispatches sprint-executor tasks in parallel.

[View traces in Cloud Trace Explorer](https://console.cloud.google.com/traces/explorer?project=ailang-multivac-dev) to see it in action.

## What it costs

The full production stack runs for approximately **$60/month**:

| Resource | Monthly Cost |
|----------|-------------|
| Coordinator (1 vCPU, always-on) | ~$20 |
| Dashboard (1 vCPU, always-on) | ~$25 |
| Agent Jobs (~100 executions x 15 min) | ~$15 |
| Pub/Sub (~300K messages) | ~$0.10 |
| Firestore (1 GB) | ~$0.18 |
| **Total** | **~$60** |

The dominant cost is Cloud Run compute. Dev environments cost less because coordinator and dashboard scale to zero when idle. AI provider API costs (Anthropic, Google) are separate and depend on your agent workload.

## First use case: autonomous website building

The first production workload running on AILANG Cloud is the [Website Builder](/blog/ailang-demos-launch) — an agent that takes a description, generates a complete website, and deploys it. Users interact through a Firebase-authenticated portal, send messages to the coordinator REST API, and the website-builder agent handles the rest.

This demonstrates the full loop: external client sends a message, coordinator dispatches an agent, agent executes in an ephemeral container, results flow back to the user through Firestore.

## Getting Started

AILANG Cloud is currently a private infrastructure repo. Here's how to bootstrap a new environment:

```bash
# Prerequisites
brew install terraform
brew install --cask google-cloud-sdk
gcloud auth login

# Bootstrap infrastructure (Phase 1: no Cloud Run yet)
cd terraform
terraform init -backend-config="bucket=ailang-multivac-tfstate" \
  -backend-config="prefix=terraform/dev"
terraform apply -var-file="environments/dev/terraform.tfvars" \
  -var="bootstrap=true"

# Build and push images (Phase 2)
gcloud builds submit --project=ailang-multivac-deploy \
  --config=cloudbuild-images.yaml \
  --substitutions="_TARGET_PROJECT=ailang-multivac-dev"

# Deploy Cloud Run services (Phase 3)
terraform apply -var-file="environments/dev/terraform.tfvars"
```

After deploy, verify everything is running:

```bash
make status   # Show deployment status
make logs     # Tail coordinator logs
```

## What's next

We're working on expanding the agent catalog — more workflow chains, more workspace integrations, and a public API for external clients to dispatch agent tasks. The Website Builder is just the first of many autonomous workflows running on this platform.

## Learn more

- [AILANG](https://github.com/sunholo-data/ailang) — the language powering the agents
- [DocParse](/blog/docparse-launch) — the first AILANG application
- [Sunholo](https://sunholo.com) — enterprise AI systems
