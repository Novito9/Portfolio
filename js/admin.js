// Basic admin login simulation
function loginAdmin() {
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  // Simple check (in production, validate on the server)
  if (username === "admin" && password === "password") {
    document.getElementById("login-section").style.display = "none";
    document.getElementById("upload-section").style.display = "block";
    return false;
  } else {
    alert("Incorrect username or password.");
    return false;
  }
}
