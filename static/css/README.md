# CSS Architecture & Documentation Standards

## Overview
This document outlines the CSS architecture, naming conventions, and documentation standards implemented across the video application's stylesheets.

## File Organization

### Core Files
- `styles.css` - Main application styles, layout, navigation
- `carousel.css` - Carousel components and interactions
- `profile.css` - Profile management interfaces
- `thumbnails.css` - Video thumbnail displays
- `theme.css` - Theme-specific styling
- `tv.css` - Large screen/TV optimizations
- `videojs.css` - Video player customizations
- `errors.css` - Error page styling

## Documentation Standards

### File Header Format
```css
/**
 * Component Name
 * ==============
 * 
 * @file filename.css
 * @description Brief description of file purpose
 * @author Video Development Team
 * @version 1.0.0
 * @created 2025-09-26
 * 
 * @dependencies
 *   - List of dependent files or libraries
 * 
 * @components
 *   - .component-name: Description
 * 
 * @responsive
 *   - Mobile: breakpoint info
 *   - Tablet: breakpoint info
 *   - Desktop: breakpoint info
 */
```

### Section Headers
```css
/* ==========================================================================
   SECTION NAME
   ========================================================================== */
```

### Component Documentation
```css
/**
 * Component description
 * 
 * @component component-name
 * @modifier .component-name--modifier - Description
 * @state :hover - Description
 * @note Additional information
 */
```

### Property Comments
```css
.component {
    property: value;                  /* Explanation of purpose */
    another-property: value;          /* Why this value is used */
}
```

## Naming Conventions

### BEM Methodology
We follow the Block Element Modifier (BEM) naming convention:

- **Block**: `.component-name`
- **Element**: `.component-name__element`
- **Modifier**: `.component-name--modifier`

### Examples
```css
/* Block */
.carousel-scroll-arrow { }

/* Element */
.carousel-scroll-arrow__icon { }

/* Modifier */
.carousel-scroll-arrow--left { }
.carousel-scroll-arrow--right { }
```

## Responsive Design

### Breakpoints
- Mobile: `< 576px`
- Small Tablet: `576px - 768px`
- Tablet: `768px - 992px`
- Desktop: `992px - 1200px`
- Large Desktop: `> 1200px`

### Mobile-First Approach
```css
/* Base styles (mobile) */
.component { }

/* Tablet and up */
@media (min-width: 768px) {
    .component { }
}

/* Desktop and up */
@media (min-width: 992px) {
    .component { }
}
```

## Dark Theme Standards

### Color Palette
- Primary Background: `#181818`
- Secondary Background: `#232323`
- Card Background: `#343a40`
- Text Primary: `#f0f0f0`
- Text Secondary: `#fff`
- Accent Blue: `#007bff`
- Success Green: `#28a745`

### Contrast Requirements
- All text must meet WCAG AA contrast requirements
- Interactive elements must have visible focus states
- Hover states should provide clear visual feedback

## Performance Considerations

### CSS Organization
1. Variables and custom properties at the top
2. Global resets and base styles
3. Layout components
4. UI components
5. Utility classes
6. Media queries grouped by breakpoint

### Optimization Guidelines
- Use `transform` and `opacity` for animations
- Minimize repaints and reflows
- Use `will-change` property sparingly
- Prefer CSS over JavaScript for simple animations

## Accessibility (A11y)

### Focus Management
```css
.interactive-element:focus {
    outline: 2px solid #007bff;
    outline-offset: 2px;
}
```

### Screen Reader Support
- Use semantic HTML where possible
- Provide proper ARIA labels
- Hide decorative elements from screen readers

### Touch Targets
- Minimum 44px × 44px for touch interfaces
- Adequate spacing between interactive elements

## Browser Support

### Target Browsers
- Chrome (latest 2 versions)
- Firefox (latest 2 versions)
- Safari (latest 2 versions)
- Edge (latest 2 versions)

### Progressive Enhancement
- Core functionality works without CSS
- Enhanced experience with modern CSS features
- Graceful fallbacks for older browsers

## Maintenance Guidelines

### Code Review Checklist
- [ ] Consistent naming conventions
- [ ] Proper documentation
- [ ] Responsive design tested
- [ ] Accessibility requirements met
- [ ] Performance impact considered
- [ ] Browser compatibility verified

### Update Process
1. Test changes locally
2. Validate CSS syntax
3. Check accessibility compliance
4. Test responsive behavior
5. Verify browser compatibility
6. Update documentation if needed