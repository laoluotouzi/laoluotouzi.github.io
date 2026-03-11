## ADDED Requirements

### Requirement: Scan attachment directories
The generator SHALL recursively scan the `docs/attachments/` directory to identify all subdirectories containing image files.

#### Scenario: Discover date directories
- **WHEN** the generator scans `docs/attachments/`
- **THEN** it SHALL identify all subdirectories (e.g., `2022/`, `2023/`, `2024/`, `2025/`, `2026/`)
- **AND** it SHALL process each subdirectory for image files

### Requirement: Extract image files
The generator SHALL extract all `1.png` files from each discovered directory.

#### Scenario: Extract PNG from date directory
- **WHEN** a directory contains a file named `1.png`
- **THEN** the generator SHALL include this image in the gallery
- **AND** it SHALL use the directory name as the date label

#### Scenario: Skip directories without images
- **WHEN** a directory does not contain `1.png`
- **THEN** the generator SHALL skip that directory
- **AND** no entry SHALL be created for that directory

### Requirement: Parse date from directory name
The generator SHALL parse date information from directory names to create chronological labels.

#### Scenario: Parse directory name as date
- **WHEN** a directory name represents a date (e.g., "2022-01-15" or similar format)
- **THEN** the generator SHALL parse the directory name as the date label
- **AND** the parsed date SHALL be displayed with the image

### Requirement: Sort images by date in descending order
The generator SHALL sort all extracted images by their parsed dates in descending chronological order (newest first).

#### Scenario: Display newest images first
- **WHEN** multiple images are extracted from different date directories
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

### Requirement: Handle missing or invalid directories
The generator SHALL gracefully handle errors when directories or files are missing or inaccessible.

#### Scenario: Continue on missing directory
- **WHEN** a specified directory does not exist
- **THEN** the generator SHALL log a warning
- **AND** it SHALL continue processing other directories
- **AND** it SHALL NOT fail the entire generation process

#### Scenario: Handle invalid date formats
- **WHEN** a directory name cannot be parsed as a date
- **THEN** the generator SHALL use the directory name as-is for the label
- **AND** it SHALL include the image in the gallery
- **AND** it SHALL place it at the end of the sorted list
