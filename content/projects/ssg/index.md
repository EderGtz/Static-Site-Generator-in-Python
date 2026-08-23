# Static Site Generator (SSG)

[< Back Home](/)

[< Projects](/projects)

A custom-built static site generator written in Python from scratch. No third-party SSG libraries. Built to deeply understand how tools like Jekyll, Hugo, and Gatsby work under the hood.

## Overview

SSG is a pure-Python static site generator that transforms a directory of Markdown files and static assets into a complete HTML website. The entire engine — from the internal node representation to the Markdown parsing logic — was built from the ground up as a learning project for the Boot.dev backend course.

## Pipeline

The engine follows a linear data transformation pipeline with strict separation of concerns:

```
Markdown Files
      |
      v
Block Parser (md_blocks.py)
  splits raw text into blocks:
  headings, paragraphs, lists,
  code blocks, blockquotes
      |
      v
Inline Converter (md_inline_converter.py)
  processes inline elements:
  bold, italic, code spans,
  links, images
      |
      v
TextNode IR (textnode.py)
  intermediate representation
  of inline elements before
  final HTML rendering
      |
      v
HTML Node Tree (htmlnode.py)
  Composite Pattern node
  hierarchy: LeafNode,
  ParentNode for nested HTML
      |
      v
Page Generator (generate_page.py)
  applies template, writes
  .html files, recurses
  directory tree
      |
      v
docs/ (output)
```

## Key Components

### HTML Node Engine

A node-based system using the Composite Pattern to represent HTML trees.

- **HTMLNode** — base class with tag, value, children, and properties
- **LeafNode** — terminal nodes with no children
- **ParentNode** — container nodes that hold children and recursively render them

This design handles arbitrary nesting depth cleanly and is testable in isolation.

### Markdown Block Parser

Splits raw Markdown text into classified blocks using regex:

- Headings (ATX `#` and setext underline styles)
- Paragraphs
- Unordered and ordered lists
- Code blocks (fenced with triple backticks)
- Blockquotes
- Inline HTML

### Inline Markdown Converter

Processes inline formatting within block text:

- Bold (**text**)
- Italic (_text_)
- Inline code (`code`)
- Links
- Images 

Uses an intermediate TextNode representation before converting to HTML nodes.

### Page Generator

- Reads a Markdown file and converts it to an HTML node tree
- Loads an HTML template with `{{ Title }}` and `{{ Content }}` placeholders
- Performs basepath replacement for asset hrefs and srcs
- Writes the final `.html` file to the output directory
- Recursively processes entire directory trees, mirroring the source structure

### Static Asset Copier

Copies the `static/` directory (CSS, images, etc.) into the output `docs/` directory so assets are served alongside generated pages.

## Project Structure

```
SSG/
├── src/
│   ├── main.py                 # entry point — orchestrates the build
│   ├── htmlnode.py             # HTML node classes (LeafNode, ParentNode)
│   ├── textnode.py             # intermediate TextNode representation
│   ├── md_to_html.py           # Markdown to HTML node tree conversion
│   ├── md_blocks.py            # block-level Markdown parsing
│   ├── md_inline_converter.py  # inline Markdown processing
│   ├── generate_page.py        # page generation + recursive directory walk
│   └── copy_static_to_public.py  # static asset copying
├── content/                    # Markdown source files
├── static/                     # CSS, images, and other assets
├── template.html               # HTML template with {{ Title }} / {{ Content }}
├── docs/                       # generated output (git-ignored)
└── main.sh / build.sh          # shell wrappers to run the generator
```

## Testing

The project includes **71 unit tests** built with Python's `unittest` framework, covering:

- HTML node rendering (LeafNode, ParentNode, nested trees)
- TextNode conversion and equality
- Markdown block classification
- Inline Markdown parsing (bold, italic, code, links, images)
- End-to-end Markdown-to-HTML conversion

Tests ensure parsing accuracy and edge-case handling across the entire pipeline.

## Technical Concepts Applied

- **Composite Pattern** — recursive HTML tree rendering via node hierarchy
- **Regex (Regular Expressions)** — advanced pattern matching for Markdown syntax
- **Recursion** — depth-first directory traversal and HTML tree generation
- **Separation of Concerns** — intermediate TextNode representation decouples parsing from rendering
- **Object-Oriented + Functional** — OOP for node structures, functional style for transformation pipelines

## Usage

Build the site from `content/` to `docs/`:

```
python3 src/main.py
```

Or use the shell wrapper:

```
./main.sh
```

Serve the output locally:

```
cd docs && python3 -m http.server 8888
```

The generator accepts an optional basepath argument for deploying to subdirectories:

```
python3 src/main.py /my-site/
```

## Repository

[github.com/EderGtz/SSG](https://github.com/EderGtz/SSG)