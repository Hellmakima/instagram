// instagram-sidebar.js
// This file defines the custom <instagram-sidebar> web component.

class InstagramSidebar extends HTMLElement {
    constructor() {
        super();
        // Attach a shadow DOM to encapsulate the component's styles and markup.
        this.attachShadow({ mode: 'open' });

        // Create a template element to hold the component's structure.
        const template = document.createElement('template');
        template.innerHTML = `
            <style>
                /* Host styles: Define the basic layout and appearance of the sidebar */
                :host {
                    display: flex; /* Use flexbox for the host element itself */
                    flex-direction: column; /* Stack children vertically */
                    width: 244px; /* Default width of the sidebar */
                    background-color: #000; /* Black background */
                    color: #e0e0e0; /* Light grey text color */
                    height: 100vh; /* Take full viewport height */
                    position: fixed; /* Keep sidebar fixed on the left */
                    left: 0;
                    top: 0;
                    padding: 8px 12px; /* Internal padding */
                    box-sizing: border-box; /* Include padding in width/height calculations */
                    border-right: 1px solid #262626; /* Subtle right border */
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
                .instagram-logo i {
                    /* Background image for the full Instagram logo */
                    background-image: url("https://static.cdninstagram.com/rsrc.php/v4/yB/r/E7m8ZCMOFDS.png");
                    background-position: 0px 0px;
                    background-size: auto;
                    width: 175px;
                    height: 51px;
                    background-repeat: no-repeat;
                    display: inline-block;
                    transition: all 0.3s ease; /* Smooth transition for logo changes */
                }

                /* Styles for the collapsed state of the Instagram logo */
                :host([collapsed]) .instagram-logo i {
                    width: 24px; /* Smaller width for collapsed state */
                    background-image: none; /* Hide the image logo */
                    /* Use Font Awesome Instagram icon when collapsed */
                    content: '\f16d'; /* Unicode for fa-instagram */
                    font-family: "Font Awesome 6 Brands"; /* Ensure correct font family is used */
                    font-size: 24px; /* Size for the icon */
                    text-align: center;
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
                    background-color: #262626; /* Darker background on hover */
                    color: #fff; /* White text on hover */
                }

                /* Active navigation item style */
                .nav-item.active {
                    font-weight: bold; /* Bold text for the active item */
                }

                /* Styles for icons within navigation items */
                .nav-item i {
                    font-size: 18px;
                    margin-right: 16px; /* Space between icon and text */
                    width: 24px; /* Fixed width for consistent icon alignment */
                    text-align: center;
                    transition: margin-right 0.3s ease; /* Smooth transition for icon margin */
                }

                /* Styles for text labels within navigation items */
                .nav-item span {
                    font-size: 16px;
                    white-space: nowrap; /* Prevent text from wrapping */
                    overflow: hidden; /* Hide overflowing text */
                    transition: opacity 0.3s ease, width 0.3s ease; /* Smooth transition for text visibility */
                }

                /* Collapsed state for navigation items */
                :host([collapsed]) .nav-item i {
                    margin-right: 0; /* Remove margin when collapsed */
                }
                :host([collapsed]) .nav-item span {
                    width: 0; /* Collapse text width */
                    opacity: 0; /* Fade out text */
                    visibility: hidden; /* Hide text from screen readers */
                }
                /* Center icons when sidebar is collapsed */
                :host([collapsed]) .nav-item {
                    justify-content: center;
                }

                /* Styles for the "More" button at the bottom */
                .more-button {
                    display: flex;
                    align-items: center;
                    padding: 12px;
                    cursor: pointer;
                    border-radius: 8px;
                    transition: background-color 0.2s ease, color 0.2s ease;
                    margin-bottom: 20px;
                }

                /* Hover effect for the "More" button */
                .more-button:hover {
                    background-color: #262626;
                    color: #fff;
                }

                /* Icon styles for the "More" button */
                .more-button i {
                    font-size: 18px;
                    margin-right: 16px;
                    width: 24px;
                    text-align: center;
                    transition: margin-right 0.3s ease;
                }

                /* Text label styles for the "More" button */
                .more-button span {
                    font-size: 16px;
                    white-space: nowrap;
                    overflow: hidden;
                    transition: opacity 0.3s ease, width 0.3s ease;
                }

                /* Collapsed state for the "More" button */
                :host([collapsed]) .more-button i {
                    margin-right: 0;
                }
                :host([collapsed]) .more-button span {
                    width: 0;
                    opacity: 0;
                    visibility: hidden;
                }
                /* Center icon when sidebar is collapsed */
                :host([collapsed]) .more-button {
                    justify-content: center;
                }
            </style>

            <div class="sidebar-top">
                <div class="instagram-logo">
                    <i aria-label="Instagram" role="img"></i>
                </div>
                <ul class="nav-list">
                    <li class="nav-item active">
                        <!-- <i class="fas fa-house"></i> -->
                        <span>Home</span>
                    </li>
                    <li class="nav-item">
                        <!-- <i class="fas fa-magnifying-glass"></i> -->
                        <span>Search</span>
                    </li>
                    <li class="nav-item">
                        <!-- <i class="fas fa-compass"></i> -->
                        <span>Explore</span>
                    </li>
                    <li class="nav-item">
                        <!-- <i class="fas fa-clapperboard"></i> -->
                        <span>Reels</span>
                    </li>
                    <li class="nav-item">
                        <!-- <i class="fas fa-paper-plane"></i> -->
                        <span>Messages</span>
                    </li>
                    <li class="nav-item">
                        <!-- <i class="fas fa-bell"></i> -->
                        <span>Notifications</span>
                    </li>
                    <li class="nav-item">
                        <!-- <i class="fas fa-plus-square"></i> -->
                        <span>Create</span>
                    </li>
                    <li class="nav-item">
                        <!-- <i class="fas fa-user"></i> -->
                        <span>Profile</span>
                    </li>
                </ul>
            </div>
            <div class="more-button">
                <!-- <i class="fas fa-bars"></i> -->
                <span>More</span>
            </div>
        `;
        // Append the template content to the shadow DOM
        this.shadowRoot.appendChild(template.content.cloneNode(true));

        // Add event listener for window resize to handle responsiveness
        window.addEventListener('resize', this.handleResize.bind(this));
        // Initial check on load to set the correct state
        this.handleResize();
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
     * Called when the custom element is removed from the DOM.
     * Cleans up the event listener to prevent memory leaks.
     */
    disconnectedCallback() {
        window.removeEventListener('resize', this.handleResize.bind(this));
    }
}

// Define the custom element, mapping the class to the tag name.
customElements.define('instagram-sidebar', InstagramSidebar);
