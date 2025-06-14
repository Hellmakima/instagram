// instagram-sidebar.js
// This file defines the custom <instagram-sidebar> web component.

class InstagramSidebar extends HTMLElement {
    constructor() {
        super();
        // Attach a shadow DOM to encapsulate the component's styles and markup.
        this.attachShadow({ mode: 'open' });

        // Define SVG icon paths for easier management.
        // All viewBoxes are typically "0 0 24 24" for consistent sizing of UI icons.

        const INSTAGRAM_GLYPH_SVG_PATH = `<path d="M12 2.982c2.937 0 3.285.011 4.445.064a6.087 6.087 0 0 1 2.042.379 3.408 3.408 0 0 1 1.265.823 3.408 3.408 0 0 1 .823 1.265 6.087 6.087 0 0 1 .379 2.042c.053 1.16.064 1.508.064 4.445s-.011 3.285-.064 4.445a6.087 6.087 0 0 1-.379 2.042 3.643 3.643 0 0 1-2.088 2.088 6.087 6.087 0 0 1-2.042.379c-1.16.053-1.508.064-4.445.064s-3.285-.011-4.445-.064a6.087 6.087 0 0 1-2.043-.379 3.408 3.408 0 0 1-1.264-.823 3.408 3.408 0 0 1-.823-1.265 6.087 6.087 0 0 1-.379-2.042c-.053-1.16-.064-1.508-.064-4.445s.011-3.285.064-4.445a6.087 6.087 0 0 1 .379-2.042 3.408 3.408 0 0 1 .823-1.265 3.408 3.408 0 0 1 1.265-.823 6.087 6.087 0 0 1 2.042-.379c1.16-.053 1.508-.064 4.445-.064M12 1c-2.987 0-3.362.013-4.535.066a8.074 8.074 0 0 0-2.67.511 5.392 5.392 0 0 0-1.949 1.27 5.392 5.392 0 0 0-1.269 1.948 8.074 8.074 0 0 0-.51 2.67C1.012 8.638 1 9.013 1 12s.013 3.362.066 4.535a8.074 8.074 0 0 0 .511 2.67 5.392 5.392 0 0 0 1.27 1.949 5.392 5.392 0 0 0 1.948 1.269 8.074 8.074 0 0 0 2.67.51C8.638 22.988 9.013 23 12 23s3.362-.013 4.535-.066a8.074 8.074 0 0 0 2.67-.511 5.625 5.625 0 0 0 3.218-3.218 8.074 8.074 0 0 0 .51-2.67C22.988 15.362 23 14.987 23 12s-.013-3.362-.066-4.535a8.074 8.074 0 0 0-.511-2.67 5.392 5.392 0 0 0-1.27-1.949 5.392 5.392 0 0 0-1.948-1.269 8.074 8.074 0 0 0-2.67-.51C15.362 1.012 14.987 1 12 1Zm0 5.351A5.649 5.649 0 1 0 17.649 12 5.649 5.649 0 0 0 12 6.351Zm0 9.316A3.667 3.667 0 1 1 15.667 12 3.667 3.667 0 0 1 12 15.667Zm5.872-10.859a1.32 1.32 0 1 0 1.32 1.32 1.32 1.32 0 0 0-1.32-1.32Z"></path>`;
        const HOME_ACTIVE_SVG_CONTENT = `<path d="M22 23h-6.001a1 1 0 0 1-1-1v-5.455a2.997 2.997 0 1 0-5.993 0V22a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1V11.543a1.002 1.002 0 0 1 .31-.724l10-9.543a1.001 1.001 0 0 1 1.38 0l10 9.543a1.002 1.002 0 0 1 .31.724V22a1 1 0 0 1-1 1Z"></path>`;
        const HOME_INACTIVE_SVG_CONTENT = `<path d="M9.005 16.545a2.997 2.997 0 0 1 2.997-2.997A2.997 2.997 0 0 1 15 16.545V22h7V11.543L12 2 2 11.543V22h7.005Z" fill="none" stroke="currentColor" stroke-linejoin="round" stroke-width="2"></path>`;

        // Updated Search SVGs
        const SEARCH_THICK_SVG_CONTENT = `<path d="M18.5 10.5a8 8 0 1 1-8-8 8 8 0 0 1 8 8Z" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="3"></path><line fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="3" x1="16.511" x2="21.643" y1="16.511" y2="21.643"></line>`;
        const SEARCH_THIN_SVG_CONTENT = `<path d="M19 10.5A8.5 8.5 0 1 1 10.5 2a8.5 8.5 0 0 1 8.5 8.5Z" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path><line fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" x1="16.511" x2="22" y1="16.511" y2="22"></line>`;

        const REELS_SVG_CONTENT = `<line fill="none" stroke="currentColor" stroke-linejoin="round" stroke-width="2" x1="2.049" x2="21.95" y1="7.002" y2="7.002"></line><line fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" x1="13.504" x2="16.362" y1="2.001" y2="7.002"></line><line fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" x1="7.207" x2="10.002" y1="2.11" y2="7.002"></line><path d="M9.763 17.664a.908.908 0 0 1-.454-.787V11.63a.909.909 0 0 1 1.364-.788l4.545 2.624a.909.909 0 0 1 0 1.575l-4.545 2.624a.91.91 0 0 1-.91 0Z" fill-rule="evenodd"></path><path d="M2 12.001v3.449c0 2.849.698 4.006 1.606 4.945.94.908 2.098 1.607 4.946 1.607h6.896c2.848 0 4.006-.699 4.946-1.607.908-.939 1.606-2.096 1.606-4.945V8.552c0-2.848-.698-4.006-1.606-4.945C19.454 2.699 18.296 2 15.448 2H8.552c-2.848 0-4.006.699-4.946 1.607C2.698 4.546 2 5.704 2 8.552Z" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path>`;
        const MESSAGE_SVG_CONTENT = `<path d="M12.003 2.001a9.705 9.705 0 1 1 0 19.4 10.876 10.876 0 0 1-2.895-.384.798.798 0 0 0-.533.04l-1.984.876a.801.801 0 0 1-1.123-.708l-.054-1.78a.806.806 0 0 0-.27-.569 9.49 9.49 0 0 1-3.14-7.175 9.65 9.65 0 0 1 10-9.7Z" fill="none" stroke="currentColor" stroke-miterlimit="10" stroke-width="1.739"></path><path d="M17.79 10.132a.659.659 0 0 0-.962-.873l-2.556 2.05a.63.63 0 0 1-.758.002L11.06 9.47a1.576 1.576 0 0 0-2.277.42l-2.567 3.98a.659.659 0 0 0 .961.875l2.556-2.049a.63.63 0 0 1 .759-.002l2.452 1.84a1.576 1.576 0 0 0 2.278-.42Z" fill-rule="evenodd"></path>`;
        const NOTIFICATIONS_SVG_CONTENT = `<path d="M16.792 3.904A4.989 4.989 0 0 1 21.5 9.122c0 3.072-2.652 4.959-5.197 7.222-2.512 2.243-3.865 3.469-4.303 3.752-.477-.309-2.143-1.823-4.303-3.752C5.141 14.072 2.5 12.167 2.5 9.122a4.989 4.989 0 0 1 4.708-5.218 4.21 4.21 0 0 1 3.675 1.941c.84 1.175.98 1.763 1.12 1.763s.278-.588 1.11-1.766a4.17 4.17 0 0 1 3.679-1.938m0-2a6.04 6.04 0 0 0-4.797 2.127 6.052 6.052 0 0 0-4.787-2.127A6.985 6.985 0 0 0 .5 9.122c0 3.61 2.55 5.827 5.015 7.97.283.246.569.494.853.747l1.027.918a44.998 44.998 0 0 0 3.518 3.018 2 2 0 0 0 2.174 0 45.263 45.263 0 0 0 3.626-3.115l.922-.824c.293-.26.59-.519.885-.774 2.334-2.025 4.98-4.32 4.98-7.94a6.985 6.985 0 0 0-6.708-7.218Z"></path>`;
        const CREATE_SVG_CONTENT = `<path d="M2 12v3.45c0 2.849.698 4.005 1.606 4.944.94.909 2.098 1.608 4.946 1.608h6.896c2.848 0 4.006-.7 4.946-1.608C21.302 19.455 22 18.3 22 15.45V8.552c0-2.849-.698-4.006-1.606-4.945C19.454 2.7 18.296 2 15.448 2H8.552c-2.848 0-4.006.699-4.946 1.607C2.698 4.547 2 5.703 2 8.552Z" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path><line fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" x1="6.545" x2="17.455" y1="12.001" y2="12.001"></line><line fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" x1="12.003" x2="12.003" y1="6.545" y2="17.455"></line>`;
        const BARS_SVG_CONTENT = `<line fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" x1="3" x2="21" y1="4" y2="4"></line><line fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" x1="3" x2="21" y1="12" y2="12"></line><line fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" x1="3" x2="21" y1="20" y2="20"></line>`;


        const template = document.createElement('template');
        template.innerHTML = `
            <style>
                /* Host styles: Define the basic layout and appearance of the sidebar */
                :host {
                    display: flex; /* Use flexbox for the host element itself */
                    flex-direction: column; /* Stack children vertically */
                    width: 244px; /* Default width of the sidebar */
                    background-color: #ffffff; /* White background for light theme */
                    color: #000000; /* Default text color is black for light theme */
                    height: 100vh; /* Take full viewport height */
                    position: fixed; /* Keep sidebar fixed on the left */
                    left: 0;
                    top: 0;
                    padding: 8px 12px; /* Internal padding */
                    box-sizing: border-box; /* Include padding in width/height calculations */
                    border-right: 1px solid #dbdbdb; /* Light subtle right border for light theme */
                    justify-content: space-between; /* Push top and bottom sections apart */
                    overflow-y: auto; /* Allow vertical scrolling if content overflows */
                    transition: width 0.3s ease; /* Smooth transition for width changes (for responsiveness) */
                }

                /* Styles for the top section of the sidebar (logo and navigation) */
                .sidebar-top {
                    flex-grow: 1; /* Allows this section to take available vertical space */
                }

                /* Instagram logo container */
                .instagram-logo {
                    display: flex;
                    align-items: center;
                    justify-content: flex-start;
                    padding: 25px 12px;
                    height: 51px;
                    overflow: hidden; /* Hide overflowing content when sidebar collapses */
                }

                /* Instagram logo image/icon */
                .instagram-logo .full-logo {
                    /* Background image for the full Instagram logo (black wordmark for light theme) */
                    background-image: url("https://www.instagram.com/static/images/web/logged_out_wordmark.png/7a252de00b20.png");
                    background-position: center; /* Center the logo within its container */
                    background-size: contain; /* Ensure the image scales down to fit */
                    width: 175px;
                    height: 51px;
                    background-repeat: no-repeat;
                    display: inline-block;
                    transition: all 0.3s ease; /* Smooth transition for logo changes */
                }

                .instagram-logo .collapsed-logo {
                    display: none; /* Hidden by default */
                    width: 24px; /* Default sizing for the collapsed SVG */
                    height: 24px;
                    color: #000000; /* Black color for the icon */
                    transition: all 0.3s ease;
                }

                /* Styles for the collapsed state of the Instagram logo */
                :host([collapsed]) .instagram-logo .full-logo {
                    display: none; /* Hide the full logo */
                }
                :host([collapsed]) .instagram-logo .collapsed-logo {
                    display: block; /* Show the collapsed SVG icon */
                }
                /* Center the logo when the sidebar is collapsed */
                :host([collapsed]) .instagram-logo {
                    justify-content: center;
                }

                /* Navigation list styles */
                .nav-list {
                    list-style: none; /* Remove default list bullets */
                    padding: 0;
                    margin: 20px 0;
                }

                /* Individual navigation item styles */
                .nav-item {
                    display: flex;
                    align-items: center;
                    padding: 12px;
                    margin-bottom: 5px;
                    cursor: pointer;
                    border-radius: 8px; /* Rounded corners for items */
                    transition: background-color 0.2s ease, color 0.2s ease; /* Smooth hover effect */
                }

                /* Hover effect for navigation items */
                .nav-item:hover {
                    background-color: #efefef; /* Light gray background on hover for light theme */
                    color: #000; /* Black text on hover for light theme */
                }

                /* Active navigation item style */
                .nav-item.active {
                    font-weight: bold; /* Bold text for the active item */
                    color: #000; /* Black text for active item in light theme */
                }

                /* Styles for SVG icons within navigation items */
                .nav-item svg,
                .more-button svg {
                    width: 24px; /* Fixed width for consistent icon alignment */
                    height: 24px; /* Fixed height for consistent icon alignment */
                    margin-right: 16px; /* Space between icon and text */
                    flex-shrink: 0; /* Prevent icon from shrinking */
                    transition: margin-right 0.3s ease; /* Smooth transition for icon margin */
                }

                /* Ensure icons use the current text color and no fill by default */
                .nav-item svg path,
                .nav-item svg line,
                .more-button svg path,
                .more-button svg line,
                .instagram-logo .collapsed-logo path {
                    fill: none; /* No fill for all icons unless specified */
                    stroke: currentColor; /* Use text color for stroked parts */
                }

                /* Specific for home icon (active/inactive states) */
                .nav-item.active .home-icon-solid {
                    display: block;
                }
                .nav-item.active .home-icon-outline {
                    display: none;
                }
                .nav-item:not(.active) .home-icon-solid {
                    display: none;
                }
                .nav-item:not(.active) .home-icon-outline {
                    display: block;
                }
                .nav-item.active .home-icon-solid path {
                    fill: currentColor; /* Fill home icon when active */
                    stroke: none; /* Remove stroke for filled home icon */
                }


                /* Specific for search icon (active/inactive states) */
                .nav-item.active .search-icon-thick {
                    display: block;
                }
                .nav-item.active .search-icon-thin {
                    display: none;
                }
                .nav-item:not(.active) .search-icon-thick {
                    display: none;
                }
                .nav-item:not(.active) .search-icon-thin {
                    display: block;
                }


                /* Styles for text labels within navigation items */
                .nav-item span {
                    font-size: 16px;
                    white-space: nowrap; /* Prevent text from wrapping */
                    overflow: hidden; /* Hide overflowing text */
                    transition: opacity 0.3s ease, width 0.3s ease; /* Smooth transition for text visibility */
                }

                /* Collapsed state for navigation items */
                :host([collapsed]) .nav-item svg,
                :host([collapsed]) .more-button svg {
                    margin-right: 0; /* Remove margin when collapsed */
                }
                :host([collapsed]) .nav-item span,
                :host([collapsed]) .more-button span {
                    width: 0; /* Collapse text width */
                    opacity: 0; /* Fade out text */
                    visibility: hidden; /* Hide text from screen readers */
                }
                /* Center icons when sidebar is collapsed */
                :host([collapsed]) .nav-item,
                :host([collapsed]) .more-button {
                    justify-content: center;
                }

                /* Styles for the "More" button at the bottom (same as nav-item for consistency) */
                .more-button {
                    display: flex;
                    align-items: center;
                    padding: 12px;
                    cursor: pointer;
                    border-radius: 8px;
                    transition: background-color 0.2s ease, color 0.2s ease;
                    margin-bottom: 20px;
                }
            </style>

            <div class="sidebar-top">
                <div class="instagram-logo">
                    <span class="full-logo" aria-label="Instagram"></span>
                    <svg class="collapsed-logo" aria-label="Instagram" fill="currentColor" height="24" role="img" viewBox="0 0 24 24" width="24">${INSTAGRAM_GLYPH_SVG_PATH}</svg>
                </div>
                <ul class="nav-list">
                    <li class="nav-item active">
                        <svg class="home-icon-solid" aria-label="Home" height="24" role="img" viewBox="0 0 24 24" width="24">${HOME_ACTIVE_SVG_CONTENT}</svg>
                        <svg class="home-icon-outline" aria-label="Home" height="24" role="img" viewBox="0 0 24 24" width="24">${HOME_INACTIVE_SVG_CONTENT}</svg>
                        <span>Home</span>
                    </li>
                    <li class="nav-item">
                        <svg class="search-icon-thick" aria-label="Search" height="24" role="img" viewBox="0 0 24 24" width="24">${SEARCH_THICK_SVG_CONTENT}</svg>
                        <svg class="search-icon-thin" aria-label="Search" height="24" role="img" viewBox="0 0 24 24" width="24">${SEARCH_THIN_SVG_CONTENT}</svg>
                        <span>Search</span>
                    </li>
                    <li class="nav-item">
                        <svg aria-label="Reels" height="24" role="img" viewBox="0 0 24 24" width="24">${REELS_SVG_CONTENT}</svg>
                        <span>Reels</span>
                    </li>
                    <li class="nav-item">
                        <svg aria-label="Messages" height="24" role="img" viewBox="0 0 24 24" width="24">${MESSAGE_SVG_CONTENT}</svg>
                        <span>Messages</span>
                    </li>
                    <li class="nav-item">
                        <svg aria-label="Notifications" height="24" role="img" viewBox="0 0 24 24" width="24">${NOTIFICATIONS_SVG_CONTENT}</svg>
                        <span>Notifications</span>
                    </li>
                    <li class="nav-item">
                        <svg aria-label="Create" height="24" role="img" viewBox="0 0 24 24" width="24">${CREATE_SVG_CONTENT}</svg>
                        <span>Create</span>
                    </li>
                    <li class="nav-item">
                        <svg aria-label="Profile" height="24" role="img" viewBox="0 0 24 24" width="24">
                            <circle cx="12" cy="7" r="4" fill="none" stroke="currentColor" stroke-width="2"></circle>
                            <path d="M4 21a8 8 0 0 1 16 0" fill="none" stroke="currentColor" stroke-width="2"></path>
                        </svg>
                        <span>Profile</span>
                    </li>
                </ul>
            </div>
            <div class="nav-item">
                <svg aria-label="More" height="24" role="img" viewBox="0 0 24 24" width="24">${BARS_SVG_CONTENT}</svg>
                <span>More</span>
            </div>
        `;
        // Append the template content to the shadow DOM
        this.shadowRoot.appendChild(template.content.cloneNode(true));

        // Event listener for window resize for responsiveness
        window.addEventListener('resize', this.handleResize.bind(this));
        this.handleResize(); // Initial check

        // Add event listeners for navigation items
        this.shadowRoot.querySelectorAll('.nav-item').forEach(item => {
            item.addEventListener('click', this.handleNavigationClick.bind(this));
        });
    }

    /**
     * Handles window resize events to adjust sidebar width and state.
     * Sets the 'collapsed' attribute on the host element if the window width is below a certain threshold (768px).
     * This attribute is then used by CSS to apply collapsed styles.
     */
    handleResize() {
        if (window.innerWidth <= 768) {
            this.setAttribute('collapsed', ''); // Add 'collapsed' attribute
        } else {
            this.removeAttribute('collapsed'); // Remove 'collapsed' attribute
        }
    }

    /**
     * Handles clicks on navigation items, setting the 'active' class.
     * @param {Event} event The click event.
     */
    handleNavigationClick(event) {
        // Remove 'active' class from all navigation items
        this.shadowRoot.querySelectorAll('.nav-item').forEach(item => {
            item.classList.remove('active');
        });
        // Add 'active' class to the clicked item
        event.currentTarget.classList.add('active');
    }

    /**
     * Called when the custom element is removed from the DOM.
     * Cleans up the event listener to prevent memory leaks.
     */
    disconnectedCallback() {
        window.removeEventListener('resize', this.handleResize.bind(this));
    }
}

// Define the custom element, mapping the class to the tag name.
customElements.define('instagram-sidebar', InstagramSidebar);