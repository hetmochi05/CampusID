// /* ============================================================
//    ADMIN DASHBOARD
//    ============================================================ */

// function toggleSidebar() {

//     const sidebar = document.getElementById("sidebar");

//     if (!sidebar) {
//         return;
//     }

//     sidebar.classList.toggle("mobile-open");
// }


// /* Close mobile sidebar when clicking outside */

// document.addEventListener("click", function (event) {

//     const sidebar = document.getElementById("sidebar");
//     const menuButton = document.querySelector(".mobile-menu");

//     if (!sidebar || !menuButton) {
//         return;
//     }

//     if (window.innerWidth > 768) {
//         return;
//     }

//     const clickedInsideSidebar =
//         sidebar.contains(event.target);

//     const clickedMenu =
//         menuButton.contains(event.target);

//     if (
//         !clickedInsideSidebar &&
//         !clickedMenu
//     ) {
//         sidebar.classList.remove("mobile-open");
//     }

// });


// /* Reset sidebar when returning to desktop */

// window.addEventListener("resize", function () {

//     const sidebar =
//         document.getElementById("sidebar");

//     if (!sidebar) {
//         return;
//     }

//     if (window.innerWidth > 768) {

//         sidebar.classList.remove("mobile-open");

//     }

// });

// =========================================================
// MOBILE SIDEBAR
// =========================================================

function toggleSidebar() {

    const sidebar = document.getElementById("sidebar");

    if (sidebar.style.display === "flex") {

        sidebar.style.display = "none";

    } else {

        sidebar.style.display = "flex";
        sidebar.style.position = "fixed";
        sidebar.style.zIndex = "2000";
        sidebar.style.width = "270px";
        sidebar.style.boxShadow =
            "0 10px 40px rgba(15, 23, 42, 0.15)";
    }
}