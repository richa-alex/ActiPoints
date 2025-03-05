//index.html
function setUserType(userType) {
    localStorage.setItem("userType", userType); // Set user type
    window.location.href = "login.html";        // Redirect to login page
}

//login.html
document.addEventListener("DOMContentLoaded", () => {     //Ensures the script only runs after the HTML is fully loaded
    //login as: ?
    let loginTitle = document.getElementById("login-title"); //document.getElementById: JS method to select an HTML element by its id.
    let userType = localStorage.getItem("userType");
    if (loginTitle) {
        loginTitle.textContent = `Login as ${userType.charAt(0).toUpperCase() + userType.slice(1)}`;
    }

    //login form
    document.getElementById("login-form")?.addEventListener("submit", (e) => {
        e.preventDefault(); //stops the form from reloading
        let email = document.getElementById("email").value;
        let password = document.getElementById("password").value;

        // Dummy credentials
        let users = {
            "admin@example.com": { password: "admin123", role: "admin", redirect: "admin-dashboard.html" },
            "faculty@example.com": { password: "faculty123", role: "faculty", redirect: "faculty-dashboard.html" },
            "student@example.com": { password: "student123", role: "student", redirect: "dashboard.html" }
        };

        if (users[email] && users[email].password === password) {
            localStorage.setItem("loggedInUser", email);
            window.location.href = users[email].redirect;
        } else {
            alert(" Invalid credentials. Try again.");
        }
    });
});

//logout
document.addEventListener("DOMContentLoaded", () => {
    const logoutBtn = document.getElementById("logout");
    if (logoutBtn) {
        logoutBtn.addEventListener("click", () => {
            localStorage.removeItem("loggedIn");
            window.location.href = "login.html";
        });
    }
});

//dashboard.html
document.addEventListener("DOMContentLoaded", () => {
    const usernameDisplay = document.getElementById("username");
    const logoutBtn = document.getElementById("logout");

    // Get user data from localStorage
    const userData = JSON.parse(localStorage.getItem("registeredUser"));
    if (userData) {
        usernameDisplay.textContent = userData.username;
    } else {
        window.location.href = "login.html"; // Redirect if not logged in
    }

    // Logout functionality
    if (logoutBtn) {
        logoutBtn.addEventListener("click", () => {
            localStorage.removeItem("loggedIn");
            alert("Logged out successfully!");
            window.location.href = "login.html";
        });
    }
});

// Function to Upload Event Poster
window.uploadEvent = function () {
    const fileInput = document.getElementById("upload-event");
    const file = fileInput.files[0];

    if (!file) {
        alert("Please select an image before uploading!");
        return;
    }

    const reader = new FileReader();
    reader.onload = function (e) {
        let li = document.createElement("li");
        let img = document.createElement("img");
        img.src = e.target.result;
        img.alt = "Uploaded Event";
        li.appendChild(img);
        document.getElementById("event-list").appendChild(li);
        alert("Event Uploaded Successfully!");
    };

    reader.readAsDataURL(file);
};

//rules
window.loadSection = function (section) {
    const content = document.getElementById("content");

    if (section === "rules") {
        content.innerHTML = `
           
        `;
    }
};

function toggleSubcategories(id) {
    let subcategoryDiv = document.getElementById(id);

    // Close all other subcategories before opening a new one
    document.querySelectorAll(".subcategories").forEach((div) => {
        if (div.id !== id) {
            div.style.display = "none";
        }
    });

    // Toggle visibility
    if (subcategoryDiv.style.display === "block") {
        subcategoryDiv.style.display = "none";
    } else {
        subcategoryDiv.style.display = "block";
    }
}

//progressbar
document.addEventListener("DOMContentLoaded", () => {
    let progressFill = document.getElementById("progress-fill");
    let pointsEarned = document.getElementById("points-earned");

    // Get points from localStorage or set default
    let totalPoints = localStorage.getItem("activityPoints") || 60;
    let goalPoints = 100; // Change to 75 for lateral entry students

    // Calculate progress percentage
    let progressPercentage = (totalPoints / goalPoints) * 100;
    progressPercentage = progressPercentage > 100 ? 100 : progressPercentage; // Max at 100%

    // Update progress bar
    progressFill.style.width = `${progressPercentage}%`;
    progressFill.textContent = `${Math.round(progressPercentage)}%`;

    // Update points display
    pointsEarned.textContent = totalPoints;
});

//profile settings
document.addEventListener("DOMContentLoaded", () => {
    let profilePic = document.getElementById("profile-pic");
    let uploadPic = document.getElementById("upload-pic");
    let profileName = document.getElementById("profile-name");
    let profileEmail = document.getElementById("profile-email");
    let profileEnrollment = document.getElementById("profile-enrollment");
    let saveProfileBtn = document.getElementById("save-profile");

    // Load saved profile data from localStorage
    profilePic.src = localStorage.getItem("profilePic") || "default-profile.png";
    profileName.value = localStorage.getItem("profileName") || "";
    profileEmail.value = localStorage.getItem("profileEmail") || "";
    profileEnrollment.value = localStorage.getItem("profileEnrollment") || "";

    // Handle profile picture upload
    uploadPic.addEventListener("change", function () {
        let file = this.files[0];
        if (file) {
            let reader = new FileReader();
            reader.onload = function (e) {
                profilePic.src = e.target.result;
                localStorage.setItem("profilePic", e.target.result);
            };
            reader.readAsDataURL(file);
        }
    });

    // Save profile info
    saveProfileBtn.addEventListener("click", () => {
        localStorage.setItem("profileName", profileName.value);
        localStorage.setItem("profileEmail", profileEmail.value);
        localStorage.setItem("profileEnrollment", profileEnrollment.value);
        alert(" Profile updated successfully!");
    });
});

// Load Admin Sections
function loadAdminSection(section) {
    let content = document.getElementById("content");
    if (section === "profile") {
        content.innerHTML = `<h2>👤 Edit Profile</h2><p>Update your profile details.</p>`;
    } else if (section === "manage-users") {
        content.innerHTML = `<h2>👥 Manage Users</h2><p>Add or remove students and faculty.</p>`;
    } else if (section === "events") {
        content.innerHTML = `<h2>📅 Update Events</h2><p>Modify upcoming event details.</p>`;
    } else if (section === "rules") {
        content.innerHTML = `<h2>📜 View Rules</h2><p>Review the ActiPoints guidelines.</p>`;
    } else if (section === "notifications") {
        content.innerHTML = `<h2>🔔 Notifications</h2><p>Check system updates and alerts.</p>`;
    }
}

// Load Faculty Sections
function loadFacultySection(section) {
    let content = document.getElementById("content");
    if (section === "profile") {
        content.innerHTML = `<h2>👤 Edit Profile</h2><p>Update your profile details.</p>`;
    } else if (section === "verify-activity") {
        content.innerHTML = `<h2>✅ Verify Activities</h2><p>Approve or reject activity submissions.</p>`;
    } else if (section === "students") {
        content.innerHTML = `<h2>📂 View Student Profiles</h2><p>Check progress and activity history.</p>`;
    } else if (section === "reports") {
        content.innerHTML = `<h2>📊 Generate Reports</h2><p>Export student data in Excel.</p>`;
    } else if (section === "rules") {
        content.innerHTML = `<h2>📜 View Rules</h2><p>Review the ActiPoints guidelines.</p>`;
    } else if (section === "notifications") {
        content.innerHTML = `<h2>🔔 Notifications</h2><p>Check system updates and alerts.</p>`;
    }
}
