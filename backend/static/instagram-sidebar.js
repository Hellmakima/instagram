// instagram-sidebar.js
class InstagramSidebar extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: 'open' }); // Attach a shadow DOM

        const template = document.createElement('template');
        template.innerHTML = `
            <style>
                :host {
                    display: block; /* Custom elements are inline by default */
                    width: 244px; /* Standard Instagram sidebar width */
                    background-color: #000; /* Dark background for sidebar */
                    color: #e0e0e0;
                    height: 100vh;
                    position: fixed;
                    left: 0;
                    top: 0;
                    padding: 8px 12px; /* Adjusted padding for better spacing */
                    box-sizing: border-box;
                    border-right: 1px solid #262626; /* Subtle border */
                    display: flex;
                    flex-direction: column;
                    justify-content: space-between; /* Pushes "More" to the bottom */
                    overflow-y: auto; /* Enable scrolling if content exceeds height */
                }

                .sidebar-top {
                    flex-grow: 1; /* Allows top section to take available space */
                }

                .instagram-logo {
                    display: flex;
                    align-items: center;
                    justify-content: flex-start; /* Align left */
                    padding: 25px 12px 25px 12px; /* Padding around the logo */
                    height: 51px; /* Match logo height */
                }

                .instagram-logo i {
                    /* Inherit styles from main page or define here if needed */
                    background-image: url("https://static.cdninstagram.com/rsrc.php/v4/yB/r/E7m8ZCMOFDS.png");
                    background-position: 0px 0px;
                    background-size: auto;
                    width: 103px; /* Smaller width for sidebar logo */
                    height: 29px; /* Smaller height for sidebar logo */
                    background-repeat: no-repeat;
                    display: inline-block;
                }

                .nav-list {
                    list-style: none;
                    padding: 0;
                    margin: 20px 0;
                }

                .nav-item {
                    display: flex;
                    align-items: center;
                    padding: 12px;
                    margin-bottom: 5px; /* Space between items */
                    cursor: pointer;
                    border-radius: 8px; /* Rounded corners for hover */
                    transition: background-color 0.2s ease, color 0.2s ease;
                }

                .nav-item:hover {
                    background-color: #262626; /* Darker on hover */
                    color: #fff;
                }
                 .nav-item.active {
                    font-weight: bold;
                }


                .nav-item .icon {
                    width: 24px; /* Icon size */
                    height: 24px;
                    margin-right: 16px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    /* Basic icon placeholder */
                    border-radius: 50%;
                    border: 1px solid #e0e0e0; /* Placeholder for icon shape */
                    font-size: 14px;
                    line-height: 1;
                }
                .nav-item.active .icon {
                    border-color: #fff; /* Active icon highlight */
                }

                .nav-item span {
                    font-size: 16px;
                    white-space: nowrap; /* Prevent text wrapping */
                }

                .more-button {
                    display: flex;
                    align-items: center;
                    padding: 12px;
                    margin-top: auto; /* Pushes it to the bottom */
                    cursor: pointer;
                    border-radius: 8px;
                    transition: background-color 0.2s ease, color 0.2s ease;
                    margin-bottom: 20px; /* Space from the bottom edge */
                }
                .more-button:hover {
                    background-color: #262626;
                    color: #fff;
                }
                .more-button .icon {
                    width: 24px;
                    height: 24px;
                    margin-right: 16px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    border-radius: 50%;
                    border: 1px solid #e0e0e0;
                    font-size: 14px;
                    line-height: 1;
                }
            </style>

            <div class="sidebar-top">
                <div class="instagram-logo">
                    <i aria-label="Instagram" role="img"></i>
                </div>
                <ul class="nav-list">
                    <li class="nav-item active">
                        <div class="icon">H</div>
                        <span>Home</span>
                    </li>
                    <li class="nav-item">
                        <div class="icon">S</div>
                        <span>Search</span>
                    </li>
                    <li class="nav-item">
                        <div class="icon">E</div>
                        <span>Explore</span>
                    </li>
                    <li class="nav-item">
                        <div class="icon">R</div>
                        <span>Reels</span>
                    </li>
                    <li class="nav-item">
                        <div class="icon">M</div>
                        <span>Messages</span>
                    </li>
                    <li class="nav-item">
                        <div class="icon">N</div>
                        <span>Notifications</span>
                    </li>
                    <li class="nav-item">
                        <div class="icon">C</div>
                        <span>Create</span>
                    </li>
                    <li class="nav-item">
                        <div class="icon">P</div>
                        <span>Profile</span>
                    </li>
                </ul>
            </div>
            <div class="more-button">
                <div class="icon">...</div>
                <span>More</span>
            </div>
        `;
        this.shadowRoot.appendChild(template.content.cloneNode(true));
    }
}

customElements.define('instagram-sidebar', InstagramSidebar);