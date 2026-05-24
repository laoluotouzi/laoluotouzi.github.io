## ADDED Requirements

### Requirement: Frontmatter extraction
The parser SHALL extract YAML frontmatter from each markdown file, including fields: title, description, banner, date, tags, and comments. The parser MUST treat frontmatter as optional content delimited by `---` at the beginning of the file.

#### Scenario: Standard frontmatter parsing
- **WHEN** a markdown file contains YAML frontmatter with title, description, banner, date, and tags fields delimited by `---`
- **THEN** the parser SHALL extract all fields and return them as a structured metadata object

#### Scenario: Missing optional frontmatter fields
- **WHEN** a markdown file contains frontmatter but is missing the banner or comments fields
- **THEN** the parser SHALL return None/default values for missing fields without raising an error

#### Scenario: No frontmatter present
- **WHEN** a markdown file does not begin with `---` and contains no YAML frontmatter
- **THEN** the parser SHALL infer the title from the first heading, set the date from the filename pattern (YYYYMMDD.md), and return empty default values for other fields

### Requirement: Markdown to HTML conversion
The parser SHALL convert markdown content (excluding frontmatter) to well-formed HTML using mistune v3. The conversion MUST support standard markdown features: headings, paragraphs, lists (ordered and unordered), links, images, bold, italic, blockquotes, tables, horizontal rules, and inline HTML.

#### Scenario: Standard markdown conversion
- **WHEN** markdown content contains headings, lists, links, images, bold, italic, blockquotes, and tables
- **THEN** the parser SHALL produce valid HTML fragments representing each element correctly

#### Scenario: Inline HTML passthrough
- **WHEN** markdown content contains raw HTML tags
- **THEN** the parser SHALL preserve the HTML tags in the output without escaping or modification

### Requirement: Code syntax highlighting
The parser SHALL apply syntax highlighting to fenced code blocks using Pygments. The parser MUST detect the language identifier from the fence info string and generate a styled HTML `<pre>` block with CSS classes for token types.

#### Scenario: Code block with language identifier
- **WHEN** a fenced code block specifies a language (e.g. ` ```python `)
- **THEN** the parser SHALL produce a `<pre><code>` block with Pygments-generated CSS class tokens for syntax highlighting

#### Scenario: Code block without language identifier
- **WHEN** a fenced code block does not specify a language
- **THEN** the parser SHALL produce a plain `<pre><code>` block without syntax highlighting classes

### Requirement: Relative path resolution
The parser SHALL resolve relative image and link paths in markdown content based on the source file's location within the `docs/` directory. All resolved paths MUST be normalized to paths relative to `docs/`.

#### Scenario: Image with relative path
- **WHEN** an image reference uses a relative path like `../../../../attachments/2025/01/20250104/banner.jpeg` from a file at `docs/blog/2025/01/20250104.md`
- **THEN** the parser SHALL resolve it to `attachments/2025/01/20250104/banner.jpeg` (relative to `docs/`)

#### Scenario: Link to another markdown file
- **WHEN** a link references another markdown file using a relative path
- **THEN** the parser SHALL resolve the path relative to `docs/` and store it for potential cross-reference processing

### Requirement: Article scanning
The parser SHALL scan the `docs/blog/` directory recursively to discover all markdown files matching the pattern `YYYYMMDD.md` organized in `YYYY/MM/` subdirectories.

#### Scenario: Full directory scan
- **WHEN** the parser scans `docs/blog/`
- **THEN** it SHALL return a list of all `.md` file paths found under any `YYYY/MM/` subdirectory, sorted by filename (which corresponds to date order)

#### Scenario: Empty directory handling
- **WHEN** a year or month subdirectory exists but contains no `.md` files
- **THEN** the parser SHALL skip that directory without error
