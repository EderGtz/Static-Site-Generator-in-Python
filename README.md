Static Site Generator (SSG) - Python

This is a Static Site Generator built from scratch using Python. It transforms raw Markdown files into a fully functional, SEO-optimized static website. This project work similar to Jekyll, Hugo, or Gatsby.

Instead of relying on existing libraries, I am building the entire engine—from the internal node representation to the complex Markdown parsing logic—to deeply understand how this kind of tools operate under the hood.
 
 Key Features

    Custom HTML Engine: Node-based system (HTMLNode, LeafNode, ParentNode) that handles complex nesting and HTML generation.

    Markdown Parser: Full support for inline Markdown (bold, italic, code, links, images) and block-level elements (headings, quotes, lists, code blocks).

    Clean Architecture: Built using Object-Oriented Programming (OOP) and Functional Programming principles for maximum maintainability.

 Technical Stack & Concepts

    Language: Python 3

    Architecture: Model-View-Controller (MVC) logic for content separation.

    Concepts Applied:

        Unit Testing: Rigorous testing using the unittest framework to ensure parsing accuracy and edge-case handling.

        Regex (Regular Expressions): Advanced pattern matching for parsing Markdown syntax into internal nodes.

        Functional Programming: Heavy use of mapping and filtering for data transformation.
