## ADDED Requirements

### Requirement: Responsive navigation bar
The navigation bar SHALL display as a horizontal scrollable strip on screens narrower than 768px, allowing users to scroll through all navigation items without wrapping or overflowing.

#### Scenario: Navigation links do not wrap on mobile
- **WHEN** the viewport width is less than 768px
- **THEN** the `.site-nav` element SHALL have `overflow-x: auto` with hidden scrollbar indicators
- **AND** all navigation links SHALL remain on a single line (`white-space: nowrap`)
- **AND** users SHALL be able to scroll horizontally to access any navigation item

#### Scenario: Header layout on mobile
- **WHEN** the viewport width is less than 768px
- **THEN** the `.site-header .container` SHALL keep site title and navigation on the same row (not stacked vertically)
- **AND** the site title SHALL be on the left, navigation on the right with horizontal scroll

### Requirement: Responsive breakpoint coverage
The CSS SHALL define media query breakpoints at 768px and 480px, with additional fine-tuning at 375px for extra-small screens.

#### Scenario: Breakpoint at 768px
- **WHEN** viewport width is 768px or less
- **THEN** the layout SHALL switch to single-column (sidebar below main content)
- **AND** the post card padding SHALL be reduced
- **AND** the post title font size SHALL be reduced

#### Scenario: Breakpoint at 480px
- **WHEN** viewport width is 480px or less
- **THEN** sidebar widget padding SHALL be reduced to 16px
- **AND** site-main padding SHALL be reduced

#### Scenario: Fine-tuning at 375px
- **WHEN** viewport width is 375px or less
- **THEN** post card thumbnail SHALL be hidden to save space
- **AND** post card layout SHALL switch to vertical (content below or without thumbnail)
- **AND** font sizes SHALL be reduced for readability on small screens
- **AND** pagination buttons SHALL be reduced in size (min-width 32px, height 32px)

### Requirement: Responsive post navigation
The post navigation (previous/next) SHALL switch to vertical stacking on small screens.

#### Scenario: Post nav stacks vertically on mobile
- **WHEN** the viewport width is less than 768px
- **THEN** `.post-nav` SHALL use `flex-direction: column`
- **AND** each `.post-nav-item` SHALL take full width (`max-width: 100%`)
- **AND** the next-post item SHALL have `text-align: left` instead of right

### Requirement: Responsive table handling in post content
Tables within post content SHALL be horizontally scrollable on small screens without breaking the page layout.

#### Scenario: Wide table scrolls horizontally
- **WHEN** a table in `.post-content` is wider than the viewport
- **THEN** the table SHALL be wrapped in a scrollable container
- **AND** the container SHALL allow horizontal scrolling without affecting the rest of the page
- **AND** the table SHALL remain fully readable via scrolling

#### Scenario: JS wraps existing tables on page load
- **WHEN** the page loads
- **THEN** the JS SHALL find all `<table>` elements inside `.post-content`
- **AND** wrap each one in a `<div class="table-wrap">` element
- **AND** skip tables that are already wrapped

### Requirement: Responsive history page
The history page year tabs and cards SHALL adapt to small screens.

#### Scenario: Year tabs scrollable on mobile
- **WHEN** the viewport width is less than 640px
- **THEN** the `.history-year-tabs` SHALL be horizontally scrollable
- **AND** the scrollbar SHALL be hidden visually
- **AND** all year tabs SHALL remain accessible via scrolling

#### Scenario: History card layout on mobile
- **WHEN** the viewport width is less than 480px
- **THEN** `.history-card-header` padding SHALL be reduced
- **AND** `.history-card-image` padding SHALL be reduced
- **AND** `.history-card-date` font size SHALL be reduced
- **AND** the lightbox close button SHALL have adequate touch target size (at least 44px)

### Requirement: Responsive sidebar on mobile
The sidebar SHALL display below main content on mobile with compact spacing.

#### Scenario: Sidebar stacks below content
- **WHEN** the viewport width is less than 768px
- **THEN** the sidebar SHALL appear below the main content
- **AND** sidebar width SHALL be 100%
- **AND** sidebar widget padding SHALL be adjusted for mobile

### Requirement: Responsive pagination on small screens
The pagination component SHALL remain usable on small screens with appropriately sized touch targets.

#### Scenario: Pagination on small screens
- **WHEN** the viewport width is less than 375px
- **THEN** pagination page buttons SHALL have minimum size of 32px by 32px
- **AND** the gap between buttons SHALL be reduced
- **AND** all pagination elements SHALL remain tappable
