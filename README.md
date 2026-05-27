# Antispam Link Shorteners 🛡️

A Python library designed to detect and block spam URL shortener domains using a blocklist.

This package provides a reliable way to check if a URL or domain belongs to a known link shortener (such as `bit.ly`,
`t.co`, `tinyurl.com`).
It helps developers protect their platforms from re-linking spam, chain shortening, and potential security risks.

The blocklist is loaded into an in-memory `set` and cached via `lru_cache`. Subsequent checks require **zero disk I/O**
overhead ($O(1)$ Complexity).

---

## 📦 Installation

Install the package using `pip`:

```bash
pip install antispam-link-shorteners
```

---

## 🚀 Usage

The library provides simple function: `link_shorteners_list`.

Use `link_shorteners_list()` to get the entire cached `set` of lowercase domains:

```python
from antispam_link_shorteners import link_shorteners_list

banned_shorteners = link_shorteners_list()
print("bit.ly" in banned_shorteners)  # True (O(1) lookup)
```

---

## 👥 Credits & Attribution

This library relies on the following open-source resources:

1. **Data Source:** The domain blocklist text file is directly sourced from
   the [PeterDaveHello/url-shorteners](https://github.com/PeterDaveHello/url-shorteners).
2. **Original library:** This library is a heavily refactored, optimized, and modernized Python alternative based on
   the [mayakyler/link-shorteners](https://github.com/mayakyler/link-shorteners).

---

## ⚖️ License

This project uses a multi-license structure to cleanly respect all upstream authors:

* **Modified library:** Licensed under the **MIT License**.
* **Original library::** Licensed under the **MIT License**.
* **Blocklist Dataset:** Distributed under the **Creative Commons Attribution-ShareAlike 4.0 International License (
  CC-BY-SA-4.0)**.