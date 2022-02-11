document.addEventListener("DOMContentLoaded", function (event) {
  const showNavbar = (toggleId, navId, bodyId, headerId) => {
    const toggle = document.getElementById(toggleId),
      nav = document.getElementById(navId),
      bodypd = document.getElementById(bodyId),
      headerpd = document.getElementById(headerId);

    // Validate that all variables exist
    if (toggle && nav && bodypd && headerpd) {
      toggle.addEventListener("click", () => {
        // show navbar
        nav.classList.toggle("show");
        // change icon
        toggle.classList.toggle("bx-x");
        // add padding to body
        bodypd.classList.toggle("body-pd");
        // add padding to header
        headerpd.classList.toggle("body-pd");
      });
    }
  };

  showNavbar("header-toggle", "nav-bar", "body-pd", "header");

  /*===== LINK ACTIVE =====*/
  const linkColor = document.querySelectorAll(".nav_link");

  function colorLink() {
    if (linkColor) {
      linkColor.forEach((l) => l.classList.remove("active"));
      this.classList.add("active");
    }
  }
  linkColor.forEach((l) => l.addEventListener("click", colorLink));

  // Your code to run since DOM is loaded and ready
});

let about = document.getElementById("about");
let aboutbtn = document.getElementById("aboutid");
let password = document.getElementById("password");
let passwordbtn = document.getElementById("passwordid");

// function hidepassword()
// {
//     getElementById("passwordid").style = .
// }

// function hideabout()
// {
//     alert();
// }

aboutbtn.onclick = function () {
  password.style.display = "none";
  passwordbtn.style.background = "none";
  passwordbtn.style.color = "black";
  passwordbtn.style.border = "none";
  about.style.display = "block";

  aboutbtn.style.background = "#0d6efd";
  aboutbtn.style.color = "white";
  aboutbtn.style.border = "#0d6efd";

  // passwordbtn.style.background="#0d6efd"
  // passwordbtn.style.color="white"
  // passwordbtn.style.border="#0d6efd"
};

passwordbtn.onclick = function () {
  password.style.display = "block";
  about.style.display = "none";
  // password.style.display='block'
  // passwordbtn.style.background="none"
  // passwordbtn.style.color="black"
  // passwordbtn.style.border="none"

  passwordbtn.style.background = "#0d6efd";
  passwordbtn.style.color = "white";
  passwordbtn.style.border = "#0d6efd";

  aboutbtn.style.background = "none";
  aboutbtn.style.color = "black";
  aboutbtn.style.border = "none";
};
