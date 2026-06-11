# Antispam Link Shorteners 🛡️

A lightweight, zero-dependency, ultra-fast Python library designed to detect and block malicious or spam URL shortener
domains using a curated blocklist.

This package provides a reliable way to check if an arbitrary URL or domain string belongs to a known link shortener (
such as `bit.ly`, `t.co`, `tinyurl.com`). It helps developers protect their platforms from re-linking spam, malicious
redirects, chain shortening, and automated bot activities.

### Key Benefits

* **High Performance:** The blocklist is parsed and loaded into an in-memory `set` upon the first call, cached
  seamlessly via `functools.lru_cache`. Subsequent checks require **zero disk I/O overhead** providing immediate $O(1)$
  lookups.
* **Smart Input Normalization:** Transparently strips whitespace, ignores casing, drops `www.` prefixes, and securely
  handles both absolute URLs (with protocols) and naked domain variants.

---

## 📦 Installation

Install the package via `pip` or using `uv`:

```bash
# Using standard pip
pip install antispam-link-shorteners

# Using uv (Recommended)
uv add antispam-link-shorteners

```

---

## 🚀 Usage

The library exposes two main public functions: `is_link_shortener` and `link_shorteners_list`.

### 1. Checking a URL (`is_link_shortener`)

The `is_link_shortener()` function takes an incoming string, normalizes it, runs security validation checks, and returns
a
boolean indicating whether the core domain is a known shortener.

```python
from antispam_link_shorteners import is_link_shortener

# Handled successfully across various input layouts:
print(is_link_shortener("bit.ly"))  # True
print(is_link_shortener("  BIT.LY  "))  # True (casing & whitespace)
print(is_link_shortener("www.bit.ly"))  # True (www stripping)
print(is_link_shortener("[https://www.bit.ly/abc?p=1](https://www.bit.ly/abc?p=1)"))  # True (path/query parsing)

# Legitimate domains pass through:
print(is_link_shortener("https://github.com"))  # False

```

#### Exception Handling & Security Guardrails

`is_link_shortener()` explicitly protects execution workflows by enforcing strict data structural criteria:

```python
from antispam_link_shorteners import is_link_shortener

try:
    is_link_shortener(12345)  # TypeError
except TypeError:
    ...

try:
    is_link_shortener("   ")  # ValueError
except ValueError:
    ...

try:
    is_link_shortener("www.ggaaa")  # ValueError
except ValueError:
    ...

```

### 2. Fetching the Underlying Raw List (`link_shorteners_list`)

Use `link_shorteners_list()` to interact directly with the underlying cached `set` of clean, lowercase blacklisted
domains:

```python
from antispam_link_shorteners import link_shorteners_list

banned_set = link_shorteners_list()
print(type(banned_set))  # <class 'set'>
print("tinyurl.com" in banned_set)  # True (O(1) memory lookup)

```

---

## 👥 Credits & Attribution

This library relies on the following open-source resources:

1. **Data Source:** The domain blocklist text file is directly sourced from
   the [PeterDaveHello/url-shorteners](https://github.com/PeterDaveHello/url-shorteners).
2. **Original Project:** This project represents a heavily refactored, type-hinted, performance-optimized, and
   modernized Python alternative inspired by [mayakyler/link-shorteners](https://github.com/mayakyler/link-shorteners).

---

## ⚖️ License

This project uses a multi-license structure to cleanly respect all upstream authors:

* **Modified library:** Licensed under the **MIT License**.
* **Original library:** Licensed under the **MIT License**.
* **Blocklist Dataset:** Distributed under the **Creative Commons Attribution-ShareAlike 4.0 International License (
  CC-BY-SA-4.0)**.