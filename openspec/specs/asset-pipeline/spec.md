## ADDED Requirements

### Requirement: Attachment file copying
The asset pipeline SHALL copy all files from `docs/attachments/` to `blog/dist/attachments/`, preserving the original directory structure (`YYYY/MM/YYYYMMDD/filename`).

#### Scenario: Full attachment copy
- **WHEN** the asset pipeline processes attachments
- **THEN** it SHALL copy every file from `docs/attachments/` to `blog/dist/attachments/` maintaining the exact same relative directory structure

#### Scenario: Binary file preservation
- **WHEN** attachment files include binary formats (JPEG, PNG, GIF, PDF, etc.)
- **THEN** the asset pipeline SHALL copy them as binary without modification, preserving file integrity

### Requirement: Static resource copying
The asset pipeline SHALL copy all files from `blog/src/static/` (CSS, JS, fonts) to `blog/dist/static/`, preserving the directory structure.

#### Scenario: CSS and JS deployment
- **WHEN** the asset pipeline runs during a build
- **THEN** all files in `blog/src/static/` SHALL be copied to `blog/dist/static/` with identical relative paths

### Requirement: Image path rewriting in HTML content
The asset pipeline SHALL ensure that all image and attachment references in rendered HTML content resolve correctly relative to the output page location. Paths from the original `docs/` directory MUST be rewritten to point to the corresponding location under `blog/dist/`.

#### Scenario: Banner image path in article detail page
- **WHEN** a post has a banner image originally at `attachments/2025/01/20250104/banner.jpeg` and the output page is at `blog/dist/posts/2025/01/20250104/index.html`
- **THEN** the banner image URL SHALL resolve to `/attachments/2025/01/20250104/banner.jpeg` or a correct relative path from the output page

#### Scenario: Inline image in post content
- **WHEN** post HTML content contains an `<img>` tag with a source originally referencing `attachments/YYYY/MM/YYYYMMDD/filename`
- **THEN** the rendered HTML SHALL contain a path that correctly points to the copied file under `blog/dist/attachments/`

### Requirement: URL-safe path encoding
The asset pipeline SHALL ensure that all generated file paths and URLs properly encode special characters (including CJK characters and spaces) using percent-encoding, while preserving the `/` path separator.

#### Scenario: Attachment filename with CJK characters
- **WHEN** an attachment filename contains Chinese characters
- **THEN** the generated URL path SHALL use percent-encoded representation of the CJK characters, and the actual file on disk SHALL keep the original name

### Requirement: Clean build output
The asset pipeline SHALL support a clean build mode where the entire `blog/dist/` directory is removed before copying files, ensuring no stale files remain from previous builds.

#### Scenario: Clean build execution
- **WHEN** a full build is triggered (not incremental)
- **THEN** the asset pipeline SHALL delete `blog/dist/` before copying any files, then recreate the directory structure and copy all fresh files
