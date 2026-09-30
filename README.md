# ⚡ Markdown Static Site Generator

> A static-site generator built from scratch in Python, with no Markdown libraries and no frameworks. It turns Markdown into HTML pages and builds a site ready for GitHub Pages.

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-121013?style=for-the-badge&logo=github&logoColor=white)
![Tests](https://img.shields.io/badge/Tests-unittest-success?style=for-the-badge)

**[Live Demo](https://rwxgauravpandey.github.io/static-site-generator/)** · **[Source Code](https://github.com/rwxgauravpandey/static-site-generator)** · **[Report a Bug](https://github.com/rwxgauravpandey/static-site-generator/issues)**

---

## Table of Contents

- [Overview](#-overview)
- [Quick Start](#-quick-start)
- [Features](#-features)
- [How It Works](#-how-it-works)
- [Example: Input to Output](#-example-input-to-output)
- [Project Structure](#-project-structure)
- [Usage](#-usage)
- [Deployment](#-deployment-to-github-pages)
- [Testing](#-testing)
- [Design Trade-offs](#-design-trade-offs)
- [Limitations and Security](#-limitations-and-security)
- [Roadmap](#-roadmap)
- [What I Learned](#-what-i-learned)
- [Author](#-author)

---

## 📌 Overview

Most static-site generators hide their internals behind a library. This project does the opposite: it implements the whole **parser → intermediate representation → renderer → build pipeline** by hand, so every step is visible and testable.

```mermaid
flowchart LR
    A[Markdown] --> B[Block Parsing]
    B --> C[Block Type Detection]
    C --> D[Inline Parsing]
    D --> E[TextNode]
    E --> F[HTMLNode]
    F --> G[HTML]
    G --> H[Template]
    H --> I[Static Site]
    I --> J[GitHub Pages]
```

**Why static?** The site is generated once at build time. There is no database and no application server, so the output can be hosted anywhere that serves files.

---

## 🚀 Quick Start

```bash
# 1. Clone
git clone https://github.com/rwxgauravpandey/static-site-generator.git
cd static-site-generator

# 2. Build the site and serve it locally
./main.sh

# 3. Open the site in your browser
# http://localhost:8888
```

**Requirements:** Python 3.x, Git, and a Unix-like shell (macOS, Linux, or WSL on Windows). No third-party packages are needed.

```bash
python3 --version   # check your Python version
```

---

## ✨ Features

| Area | What it does |
|---|---|
| **Markdown parsing** | Headings, paragraphs, bold, italic, inline code, code blocks, blockquotes, ordered and unordered lists, links, images |
| **Block type detection** | Classifies each block with a `BlockType` enum: `paragraph`, `heading`, `code`, `quote`, `unordered_list`, `ordered_list` |
| **Regex inline parsing** | Recognizes `**bold**`, `_italic_`, `` `code` ``, `[link](url)`, and `![image](url)` |
| **Intermediate representation** | Markdown becomes `TextNode` objects, then an `HTMLNode` tree, and only then HTML |
| **Templates** | Inserts the generated title and content into a reusable `template.html` |
| **Recursive page generation** | Walks any depth of `content/` and mirrors it in the output folder |
| **Static assets** | Recursively copies `static/` (CSS, images) into the built site |
| **Configurable base path** | Works under `/` or under a repository path like `/static-site-generator/` |
| **Testing** | Unit tests for the parsing and node logic, run with `test.sh` |
| **GitHub Pages ready** | The production build writes the deployable site to `docs/` |

---

## 🧠 How It Works

### 1. Split into blocks

The document is divided into block-level sections.

```markdown
# My Blog

This is **my first post**.

- Python
- AI
```

```text
Block 1 → Heading
Block 2 → Paragraph
Block 3 → Unordered list
```

### 2. Detect block types

| Markdown | Block type |
|---|---|
| `# Heading` | `HEADING` |
| Plain text | `PARAGRAPH` |
| `> Quote` | `QUOTE` |
| `- Item` | `UNORDERED_LIST` |
| `1. Item` | `ORDERED_LIST` |
| Text wrapped in triple backticks | `CODE` |

### 3. Parse inline Markdown

Regular expressions split text into typed `TextNode`s:

```text
"This is **bold** and _italic_."

TextNode("This is ", TEXT)
TextNode("bold",     BOLD)
TextNode(" and ",    TEXT)
TextNode("italic",   ITALIC)
TextNode(".",        TEXT)
```

### 4. Convert to an HTML node tree

Each `TextNode` becomes a matching `HTMLNode`, and blocks become parent nodes:

```text
HTMLNode("p")
├── "This is "
├── HTMLNode("strong") → "bold"
├── " and "
├── HTMLNode("em")     → "italic"
└── "."
```

### 5. Render and apply the template

The tree is serialized to an HTML string, then placed into `template.html`, which uses two placeholders:

```html
<title>{{ Title }}</title>

<article>
    {{ Content }}
</article>
```

### 6. Write the page

The result is written to the output folder, keeping the same directory layout as `content/`.

---

## 🔄 Example: Input to Output

**Input** (`content/index.md`)

```markdown
# Hello

This is **my first post**.
```

**Output** (`docs/index.html`, simplified)

```html
<title>Hello</title>

<article>
    <div>
        <h1>Hello</h1>
        <p>This is <strong>my first post</strong>.</p>
    </div>
</article>
```

---

## 📂 Project Structure

```text
static-site-generator/
├── src/
│   ├── main.py              # entry point: runs the build
│   ├── textnode.py          # TextNode and TextType
│   ├── htmlnode.py          # HTMLNode, LeafNode, ParentNode
│   ├── inline_markdown.py   # regex-based inline parsing
│   ├── markdown_blocks.py   # block splitting and BlockType detection
│   ├── page_generator.py    # template + recursive page generation
│   ├── copystatic.py        # recursive static asset copying
│   └── test_*.py            # unit tests for each module
├── content/                 # Markdown source
│   ├── index.md
│   ├── contact/
│   └── blog/
├── static/                  # copied as-is into the built site
│   ├── index.css
│   └── images/
├── docs/                    # generated site, published by GitHub Pages
├── template.html            # page template
├── main.sh                  # build and serve locally
├── build.sh                 # production build into docs/
├── test.sh                  # run the unit tests
└── README.md
```

Content maps directly to output pages:

```text
content/blog/python/index.md   →   docs/blog/python/index.html
```

---

## 🖥️ Usage

| Task | Command |
|---|---|
| Build and serve locally | `./main.sh` |
| Production build into `docs/` | `./build.sh` |
| Run tests | `./test.sh` |
| Build with a custom base path | `python3 src/main.py "/static-site-generator/"` |

To run the unit tests directly:

```bash
python3 -m unittest discover -s src
```

> The local build and the production build write to different folders and use different base paths. See `main.sh` and `build.sh` for the exact settings.

---

## 🌐 Deployment to GitHub Pages

```text
Write Markdown → ./build.sh → docs/ generated → commit → push → GitHub Pages publishes docs/
```

1. Write or edit Markdown in `content/`.
2. Run `./build.sh`. It builds into `docs/` with the repository base path.
3. Commit and push the changes, including `docs/`.
4. On GitHub, open **Settings → Pages**, and set the source to the `main` branch and the `/docs` folder.
5. The site is published at `https://rwxgauravpandey.github.io/static-site-generator/`.

**Why a base path?** A project site lives at `/static-site-generator/`, not `/`. Without the base path, links to CSS, images, and other pages would break. The generator rewrites those URLs from the value you pass in.

---

## 🧪 Testing

```bash
./test.sh
```

Parsing bugs spread quickly through a pipeline, because a mistake in block splitting or inline parsing changes every later stage. Each core module therefore has its own test file:

| Test file | Covers |
|---|---|
| `test_textnode.py` | `TextNode` behavior |
| `test_htmlnode.py` | `HTMLNode` and HTML serialization |
| `test_inline_markdown.py` | Inline parsing: bold, italic, code, links, images |
| `test_markdown_blocks.py` | Block splitting and block type detection |

---

## ⚖️ Design Trade-offs

This project favors **learning and clarity** over production completeness.

| Decision | Why | Trade-off |
|---|---|---|
| Custom Markdown parser | Understand parsing internals | Not the full Markdown spec |
| Regex for inline syntax | Simple for the supported syntax | Nested Markdown is hard to handle |
| `TextNode` layer | Separates parsing from rendering | An extra abstraction |
| `HTMLNode` tree | Structured, testable HTML generation | More objects and code |
| Recursive directory traversal | Handles any folder depth | More code than high-level helpers |
| Custom template replacement | No dependencies | Weaker than a full template engine |
| Static generation | Fast, simple hosting | No runtime dynamic behavior |
| GitHub Pages | Free, simple hosting | Base-path constraints |
| Python `http.server` | Zero-setup local testing | Not a production server |

---

## 🔐 Limitations and Security

This is an educational implementation, not a hardened Markdown engine. A production system would also need:

- HTML escaping and XSS prevention
- URL validation
- Safe handling of raw HTML and malicious Markdown
- Validation of generated file paths

Only use it on Markdown you trust.

---

## 🗺️ Roadmap

**Parsing**
- [ ] Nested Markdown structures
- [ ] A more formal tokenizer and parser
- [ ] Better HTML escaping and sanitization

**Content**
- [ ] Front matter and metadata (author, date, tags)
- [ ] Syntax highlighting for code blocks
- [ ] RSS/Atom feed and sitemap generation

**Build system**
- [ ] Incremental builds with file-change detection and caching
- [ ] Parallel page generation
- [ ] A richer template system

**Quality and delivery**
- [ ] GitHub Actions CI/CD
- [ ] Deployment validation
- [ ] More end-to-end tests

---

## 🎯 What I Learned

Building this showed me how a simplified compiler-like pipeline is designed and implemented.

- **Parsing:** tokenization, regular expressions, block vs inline parsing
- **Design:** intermediate representations, AST-like trees, object-oriented design, enums
- **Engineering:** recursion, filesystem traversal, file I/O, exception handling
- **Quality:** unit testing
- **Delivery:** template rendering, CLI arguments, build scripts, base-path handling, GitHub Pages deployment

---

## 🧩 Built With

Python · Regular Expressions · HTML5 · CSS · Bash · `unittest` · `http.server` · Git and GitHub · GitHub Pages · WSL

---

## 👨‍💻 Author

**Gaurav Pandey**, AI/ML Engineer

Built as part of my journey into Python, software engineering, and production-oriented development. This project was a hands-on exercise in understanding how a static-site generator works underneath the abstractions.

[GitHub: @rwxgauravpandey](https://github.com/rwxgauravpandey)

---

**The core idea:** `Markdown → Parser → Nodes → HTML → Static Site`
