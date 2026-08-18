# Ahmed Hassan

**Principal AI Systems & Security Architect | Forward Deployed Engineer (FDE)**
Founder of [A2Z SOC](https://a2zsoc.com) | Email: [ahmed.alaa.hassan25@gmail.com](mailto:ahmed.alaa.hassan25@gmail.com) | [LinkedIn](https://www.linkedin.com/in/ahmed-hassan-f11/)

> *Architecting Deterministic, Zero-Trust Infrastructure for Autonomous AI Agents at Production Scale.*

---

## The Core Architectural Focus: The AI Agent Execution Plane

Rather than a scattered assortment of tools, my work is strictly focused on a single unified mission: **building the end-to-end execution, security, and runtime plane for Autonomous AI Agents** — from the Linux Kernel (Ring 0) to Deep Learning Compilers, Tool Sandboxes, and ISO 42001 Governance.

```
+------------------------------------------------------------------------------------------+
|                           THE ENTERPRISE AGENT EXECUTION PLANE                           |
+------------------------------------------------------------------------------------------+
| 1. MACRO GOVERNANCE & ORCHESTRATION                                                      |
|    - GRC_Claw (ISO 42001, Anti-Swarm WAF, MAVLink Robotics)                              |
|      https://github.com/AAH20/GRC_Claw                                                   |
|                                                                                          |
| 2. AGENT NETWORK & DISTRIBUTED CONSENSUS                                                 |
|    - Agent-Mesh-Sidecar (In-process A2A Service Mesh & Discovery)                        |
|      https://github.com/AAH20/agent-mesh-sidecar                                         |
|    - BFT-Agent-Consensus (PBFT Byzantine Fault Tolerant Quorums)                         |
|      https://github.com/AAH20/bft-agent-consensus                                        |
|                                                                                          |
| 3. AGENT MEMORY, STATE & EVALUATION                                                      |
|    - Agent-WAL (ACID Write-Ahead Logging & Deterministic Replay)                         |
|      https://github.com/AAH20/agent-wal                                                  |
|    - Graph-RAG-Guard (Knowledge Graph & Multi-Hop Poisoning Defense)                     |
|      https://github.com/AAH20/graph-rag-guard                                            |
|    - Agent-Eval-Guard (In-situ Continuous Evaluation & Drift CI Gate)                    |
|      https://github.com/AAH20/agent-eval-guard                                           |
|                                                                                          |
| 4. TOOL-CALLING FIREWALL & SECURITY BOUNDARY                                             |
|    - Agent-Schema-Firewall (MCP & OpenAPI Dynamic Schema Defense)                        |
|      https://github.com/AAH20/agent-schema-firewall                                      |
|    - MCP-Shield (Zero-Trust MCP Tool Firebox & Entropy Guard)                            |
|      https://github.com/AAH20/mcp-shield                                                 |
|    - Zero-Leak-DLP (Outbound Token & PII Exfiltration Firewall)                          |
|      https://github.com/AAH20/zero-leak-dlp                                               |
|    - Agent-JIT-IAM (Ephemeral Just-In-Time Micro-Credentials & ZSP)                       |
|      https://github.com/AAH20/agent-jit-iam                                              |
|                                                                                          |
| 5. LOW-LEVEL RUNTIME, COMPUTE & KERNEL CONTAINMENT                                       |
|    - Agent-Kill-Switch (Out-of-band Dead-Man Sentinel & Quorum Breaker)                   |
|      https://github.com/AAH20/agent-kill-switch                                          |
|    - Kernel-Agent-eBPF (Ring-0 Linux Kernel Syscall Probe & Guard)                       |
|      https://github.com/AAH20/kernel-agent-ebpf                                          |
|    - Aegis-Runtime (Sub-millisecond ActionGate & SHA-256 Ledger)                         |
|      https://github.com/AAH20/aegis-runtime                                              |
|    - Agent-FinOps (Autonomous KV-Cache & GPU Tokenomics Router)                          |
|      https://github.com/AAH20/agent-finops                                               |
+------------------------------------------------------------------------------------------+
```

---

### 1. Macro Governance & Orchestration
- [GRC_Claw](https://github.com/AAH20/GRC_Claw): ISO 42001 AI Risk Governance, Anti-Swarm WAF, MAVLink UAS Robotics, and A2Z SOC platform.

### 2. Agent Network & Distributed Consensus
- [agent-mesh-sidecar](https://github.com/AAH20/agent-mesh-sidecar): In-process A2A service mesh, semantic discovery, sub-0.05ms routing, and circuit breaking.
- [bft-agent-consensus](https://github.com/AAH20/bft-agent-consensus): Practical Byzantine Fault Tolerance (PBFT 2f+1) quorum engine eliminating sycophancy cascades.

### 3. Agent Memory, State & Evaluation
- [agent-wal](https://github.com/AAH20/agent-wal): Embedded 2-Phase Commit Write-Ahead Log for zero-loss crash recovery and deterministic time-travel replay.
- [graph-rag-guard](https://github.com/AAH20/graph-rag-guard): Sub-millisecond Knowledge Graph Oracle Poisoning & Hop-wise GraphRAG defense firewall with SHA-256 Merkle lineage.
- [agent-eval-guard](https://github.com/AAH20/agent-eval-guard): In-situ sub-0.05ms faithfulness evaluator, CUSUM statistical drift detector, and auto-regression CI gate.

### 4. Tool-Calling Firewall & Identity Boundary
- [agent-schema-firewall](https://github.com/AAH20/agent-schema-firewall): Dynamic MCP & OpenAPI schema poisoning, AgenTRIM tool shadowing, prompt injection, and hidden backdoor parameter pruner.
- [mcp-shield](https://github.com/AAH20/mcp-shield): Zero-Trust runtime firebox for Model Context Protocol with Shannon entropy baselines and AST quarantine.
- [zero-leak-dlp](https://github.com/AAH20/zero-leak-dlp): Sub-millisecond outbound DLP firewall intercepting API keys, AWS tokens, JWTs, and auto-redacting PII.
- [agent-jit-iam](https://github.com/AAH20/agent-jit-iam): Zero Standing Privilege (ZSP) JIT ephemeral token minter (plugs into AWS STS / K8s RBAC) to prevent silent privilege escalation.

### 5. Low-Level Runtime, Compute & Kernel Containment
- [agent-kill-switch](https://github.com/AAH20/agent-kill-switch): Out-of-band Dead-Man Switch & M-of-N human quorum breaker for AI Containment & AI Kill Switch Act (2026) compliance.
- [kernel-agent-ebpf](https://github.com/AAH20/kernel-agent-ebpf): Ring-0 Linux kernel eBPF C probes intercepting syscalls, preventing container escapes & unauthorized filesystem access.
- [aegis-runtime](https://github.com/AAH20/aegis-runtime): Pure stdlib 1-line ActionGate with tamper-proof SHA-256 state receipts.
- [agent-finops](https://github.com/AAH20/agent-finops): Autonomous KV-cache prefix hashing tracker slashing 85% prefill compute & capping runaway agent billing loops.

---

## Core Deep Learning & Systems Compilers Contributions (82 Shipped Upstream PRs)

The agent execution plane is anchored by deep contributions directly to the runtimes and compilers powering modern AI:

- **PyTorch Core (`pytorch/pytorch`):** AOTAutograd, TorchDynamo, TorchInductor, ATen, FSDP2.
- **vLLM Core (`vllm-project/vllm`):** PagedAttention v2 inference engine memory stability.
- **SGLang Engine (`sgl-project/sglang`):** RadixCache Trie memory management optimizations.
- **Microsoft DeepSpeed (`deepspeedai/DeepSpeed`):** MoE & ZeRO Inference engines.
- **Google DeepMind JAX (`jax-ml/jax`):** Pallas TPU/GPU custom kernel stability.
- **NVIDIA TensorRT-LLM (`NVIDIA/TensorRT-LLM`):** C++ Model Runner pipeline.
- **CNCF OpenCost (`opencost/opencost`):** Kubernetes Cloud & GPU FinOps gates.
- **PydanticAI (`pydantic/pydantic-ai`):** Agent Tool & Schema execution engines.

---

## Engineering Standards
- **Zero Supply-Chain Dependency Risk:** 100% standard library implementations to prevent nested dependency attacks in air-gapped/enterprise environments.
- **Sub-Millisecond Overhead:** Every layer operates under 0.05ms latency budgets.
- **Cryptographic Immutability:** SHA-256 chained event receipts standard across all engines for **ISO 42001, SOC 2 Type II, and EU AI Act (Art. 50)** audit readiness.
