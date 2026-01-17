# Static Site Generator (SSG) - Python

This is a Static Site Generator built from scratch using Python. It transforms raw Markdown files into a fully functional static website. This project works similarly to Jekyll, Hugo, or Gatsby.

Instead of relying on existing libraries, I built the entire engine—from the internal node representation to the complex Markdown parsing logic—to deeply understand how these tools operate under the hood.

## How it Works (The Pipeline)

The engine follows a linear data transformation pipeline to ensure data integrity and strict separation of concerns:

<img width="815" height="66" alt="image" src="https://github.com/user-attachments/assets/d293e72f-d82b-4aec-af70-7616814280a3" />

## Key Features

* **Custom HTML Engine:** A node-based system utilizing `HTMLNode`, `LeafNode`, and `ParentNode` that handles complex nesting through the Composite Pattern.
* **Markdown Parser:** Full support for inline Markdown (bold, italic, code, links, images) and block-level elements (headings, quotes, lists, code blocks).
* **Recursive Generation:** Automatically mirrors complex directory structures from source to destination, handling both content and static assets.
* **Clean Architecture:** Built using Object-Oriented Programming (OOP) and Functional Programming principles for maximum maintainability.

## Technical Stack & Concepts

* **Language:** Python 3.
* **Architecture:** Separation of concerns using an intermediate representation (`TextNode`) before final HTML rendering.
* **Concepts Applied:**
    * **Unit Testing:** Rigorous testing using the `unittest` framework to ensure parsing accuracy and edge-case handling. 71 tests created. 
    * **Regex (Regular Expressions):** Advanced pattern matching for parsing Markdown syntax into internal nodes.
    * **Recursion:** Depth-first traversal for both HTML tree rendering and directory processing.

## Project Structure

* `main.py`: Entry point that orchestrates the build process.
* `html_node.py`: Core classes for HTML tree representation.
* `textnode.py`: Intermediate representation for inline elements.
* `md_to_html.py`: Logic for converting full Markdown documents into HTML node trees.
* `md_blocks.py` & `md_inline_converter.py`: Logic for Markdown parsing and classification.
* `generate_page.py`: File system handling and template integration.
