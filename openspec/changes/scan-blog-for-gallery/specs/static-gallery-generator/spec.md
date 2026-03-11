## REMOVED Requirements

### Requirement: Scan attachment directories
**Reason**: 改为从博客 Markdown 文件中提取图片引用，不再直接扫描附件目录
**Migration**: 使用新的"Scan blog markdown files"需求

### Requirement: Extract image files
**Reason**: 图片提取逻辑改为从 Markdown 文件中解析图片引用，不再直接从目录中提取文件
**Migration**: 使用新的"Extract image references from markdown"需求

### Requirement: Parse date from directory name
**Reason**: 日期解析改为从 Markdown 文件路径中提取，而不是从目录名称解析
**Migration**: 使用新的"Parse date from file path"需求

### Requirement: Handle missing or invalid directories
**Reason**: 错误处理改为针对 Markdown 文件，而不是目录结构
**Migration**: 使用新的"Handle missing or invalid markdown files"需求

## ADDED Requirements

### Requirement: Scan blog markdown files
The generator SHALL recursively scan the `docs/blog/` directory to identify all Markdown files (`.md`) for processing.

#### Scenario: Discover markdown files
- **WHEN** the generator scans `docs/blog/`
- **THEN** it SHALL identify all `.md` files recursively
- **AND** it SHALL filter files containing "老罗投资周记" keyword
- **AND** it SHALL process only the filtered files for image extraction

### Requirement: Extract image references from markdown
The generator SHALL extract image references from Markdown files by parsing Markdown image syntax.

#### Scenario: Extract image reference from markdown content
- **WHEN** a Markdown file contains an image reference with the pattern `![目前持仓](../../../attachments/YYYY/MM/DDDDDD/1.png)`
- **THEN** the generator SHALL extract the image path from the reference
- **AND** it SHALL use the extracted path for the gallery
- **AND** it SHALL parse the date from the image path

#### Scenario: Skip files without image references
- **WHEN** a Markdown file does not contain the expected image reference pattern
- **THEN** the generator SHALL skip that file
- **AND** no entry SHALL be created for that file

### Requirement: Convert relative path to public URL
The generator SHALL convert relative image paths to publicly accessible URLs.

#### Scenario: Generate public URL
- **WHEN** an image path is extracted (e.g., `../../../attachments/2026/03/20260307/1.png`)
- **THEN** the generator SHALL convert it to `https://invest.zdyi.com/attachments/2026/03/20260307/1.png`
- **AND** the URL SHALL be used in the generated HTML gallery

### Requirement: Parse date from file path
The generator SHALL parse date information from the extracted image file path.

#### Scenario: Parse date from image path
- **WHEN** an image path contains a date pattern (e.g., `20260307` from `../../../attachments/2026/03/20260307/1.png`)
- **THEN** the generator SHALL extract and parse the date
- **AND** the parsed date SHALL be used for sorting and display
- **AND** the date SHALL be displayed in the gallery

### Requirement: Extract metadata from markdown
The generator SHALL extract additional metadata from Markdown files to enhance the gallery display.

#### Scenario: Extract blog post title
- **WHEN** processing a Markdown file
- **THEN** the generator SHALL extract the title from the file
- **AND** the title SHALL be available for gallery display

#### Scenario: Extract blog post date
- **WHEN** processing a Markdown file
- **THEN** the generator SHALL extract the date from the file path or frontmatter
- **AND** the date SHALL be used for chronological sorting

### Requirement: Handle missing or invalid markdown files
The generator SHALL gracefully handle errors when Markdown files are missing, inaccessible, or malformed.

#### Scenario: Continue on missing file
- **WHEN** a specified Markdown file does not exist
- **THEN** the generator SHALL log a warning
- **AND** it SHALL continue processing other files
- **AND** it SHALL NOT fail the entire generation process

#### Scenario: Handle malformed image references
- **WHEN** a Markdown file contains an invalid image reference pattern
- **THEN** the generator SHALL log a warning
- **AND** it SHALL skip that file
- **AND** it SHALL continue processing other files

## MODIFIED Requirements

### Requirement: Sort images by date in descending order
The generator SHALL sort all extracted images by their parsed dates in descending chronological order (newest first).

#### Scenario: Display newest images first
- **WHEN** multiple images are extracted from different Markdown files
- **THEN** the generated gallery SHALL display images sorted by date
- **AND** the most recent date SHALL appear first
- **AND** the oldest date SHALL appear last

### Requirement: Generate waterfall layout HTML
The generator SHALL produce a static HTML page with a waterfall (masonry) layout for displaying images.

#### Scenario: Create responsive waterfall grid
- **WHEN** the generator creates the HTML output
- **THEN** it SHALL implement a CSS grid or flexbox-based waterfall layout
- **AND** the layout SHALL be responsive across different screen sizes
- **AND** images SHALL flow naturally in columns

#### Scenario: Include images with date labels
- **WHEN** rendering the gallery
- **THEN** each image SHALL be displayed with its corresponding date label
- **AND** images SHALL maintain their aspect ratio
- **AND** clicking on an image SHALL open the full-size version

### Requirement: Output to specified location
The generator SHALL write the generated HTML page to a specified output path.

#### Scenario: Write to history directory
- **WHEN** the generator completes processing
- **THEN** it SHALL write the HTML output to `history/static/index.html`
- **AND** the file SHALL be a complete, standalone HTML page
- **AND** all necessary CSS SHALL be embedded in the HTML
