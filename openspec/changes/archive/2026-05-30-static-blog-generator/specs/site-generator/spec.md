## ADDED Requirements

### Requirement: Article detail page generation
The generator SHALL produce an individual HTML page for each blog post, rendered via Jinja2 template, containing the post title, date, tags, banner image, and full HTML content. Each page MUST be written to `blog/dist/posts/YYYY/MM/YYYYMMDD/index.html`.

#### Scenario: Standard article page
- **WHEN** a parsed post has title, date, tags, banner, and HTML content
- **THEN** the generator SHALL render a complete HTML page at `blog/dist/posts/YYYY/MM/YYYYMMDD/index.html` containing all metadata and content

#### Scenario: Article without banner
- **WHEN** a parsed post has no banner field
- **THEN** the generator SHALL render the article page without a banner image section, using a fallback layout

### Requirement: Homepage with paginated post list
The generator SHALL produce a homepage at `blog/dist/index.html` displaying the most recent posts in reverse chronological order with pagination. Each page SHALL display a configurable number of posts (default 10) with title, date, description, and banner thumbnail.

#### Scenario: First page rendering
- **WHEN** the generator renders the homepage
- **THEN** it SHALL output `blog/dist/index.html` with the 10 most recent posts, each showing title, date, description, and banner, with a "next page" link if more posts exist

#### Scenario: Pagination navigation
- **WHEN** more than 10 posts exist
- **THEN** the generator SHALL create additional pages at `blog/dist/page/N/index.html` (N starting from 2), each with "previous" and "next" navigation links

### Requirement: Tag index pages
The generator SHALL produce an index page listing all unique tags, and individual pages for each tag showing all posts associated with that tag in reverse chronological order.

#### Scenario: Tag listing page
- **WHEN** the generator builds tag pages
- **THEN** it SHALL produce `blog/dist/tags/index.html` listing all unique tags with their post counts

#### Scenario: Individual tag page
- **WHEN** a tag has associated posts
- **THEN** the generator SHALL produce `blog/dist/tags/<tag-slug>/index.html` listing all posts for that tag, sorted by date descending

### Requirement: Archive pages by year and month
The generator SHALL produce archive pages organized by year and by year-month, listing all posts in the respective time period in reverse chronological order.

#### Scenario: Year archive page
- **WHEN** the generator builds archive pages
- **THEN** it SHALL produce `blog/dist/archive/YYYY/index.html` for each year containing posts, listing all posts in that year

#### Scenario: Month archive page
- **WHEN** a specific year-month combination has posts
- **THEN** the generator SHALL produce `blog/dist/archive/YYYY/MM/index.html` listing all posts in that month

### Requirement: RSS feed generation
The generator SHALL produce an RSS 2.0 compliant XML feed at `blog/dist/feed.xml` containing the most recent posts (up to 20) with title, link, description, publication date, and content summary.

#### Scenario: RSS feed output
- **WHEN** the generator builds the site
- **THEN** it SHALL produce `blog/dist/feed.xml` with valid RSS 2.0 markup containing the latest 20 posts with title, absolute URL, description, and pubDate

#### Scenario: Feed with fewer than 20 posts
- **WHEN** the total number of posts is less than 20
- **THEN** the RSS feed SHALL include all available posts

### Requirement: Template rendering with Jinja2
The generator SHALL use Jinja2 templates stored in `blog/src/templates/` with template inheritance. A base template SHALL define the common layout (head, header, footer), and page-specific templates SHALL extend it.

#### Scenario: Template inheritance
- **WHEN** rendering any page type
- **THEN** the page template SHALL extend `base.html` and override the content block while inheriting the common head, header, and footer sections

### Requirement: CLI build interface
The generator SHALL provide a command-line interface via `python3 blog/src/generator.py` with a `build` subcommand that performs a full site build and a `clean` subcommand that removes the `blog/dist/` directory.

#### Scenario: Full build
- **WHEN** the user runs `python3 blog/src/generator.py build`
- **THEN** the generator SHALL scan all posts, parse them, render all pages, copy assets, and produce the complete site in `blog/dist/`

#### Scenario: Clean output
- **WHEN** the user runs `python3 blog/src/generator.py clean`
- **THEN** the generator SHALL delete the entire `blog/dist/` directory
