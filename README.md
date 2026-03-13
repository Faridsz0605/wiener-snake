# Wiener-snake

![Python](https://img.shields.io/badge/python-3.12-blue?logo=python&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-CPU-ee4c2c?logo=pytorch&logoColor=white)
![uv](https://img.shields.io/badge/uv-package%20manager-5c5cff?logo=astral&logoColor=white)
![License: MIT](https://img.shields.io/badge/license-MIT-green)

An educational reinforcement learning project by [wiener-studios], originally born from a collaboration with [@Gandrenix](https://github.com/Gandrenix).

> **Shoutout to the real brain**
> Tutoring and original concept by [@patrickloeber](https://github.com/patrickloeber).
> Original source: [snake-ai-pytorch](https://github.com/patrickloeber/snake-ai-pytorch)

---

## About

Snake AI trained via reinforcement learning using PyTorch. Built with `pygame` for rendering and designed to run on **CPU-only** machines — no GPU required.

---

## Stack

| Tool | Purpose |
|------|---------|
| Python 3.12 | Runtime |
| PyTorch (CPU) | Reinforcement learning |
| pygame | Game rendering |
| numpy | Array operations |
| matplotlib | Training curve visualization |
| mise | Tool version management |
| uv | Dependency management |

---

## Getting started

### Prerequisites

- [mise](https://mise.jdx.dev) installed

### Setup

```bash
mise install        # installs Python 3.12 + uv
mise run install    # syncs dependencies via uv
```

### Run

```bash
mise run train      # train the AI agent
mise run run        # play snake with trained model
```

---

## License

MIT — see [LICENSE](LICENSE) for details. Code is open source and free to use.
