// Main JavaScript file for Puppi Tinder

// Global variables
const authToken = localStorage.getItem("authToken")
let currentUser = JSON.parse(localStorage.getItem("currentUser") || "null")

// Initialize app when DOM is loaded
document.addEventListener("DOMContentLoaded", () => {
  initializeApp()
  setupEventListeners()
  updateAuthUI()
})

// Initialize the application
function initializeApp() {
  // Check if user is logged in
  if (authToken) {
    validateToken()
  }

  // Initialize tooltips if Bootstrap is available
  if (typeof window.bootstrap !== "undefined") {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map((tooltipTriggerEl) => new window.bootstrap.Tooltip(tooltipTriggerEl))
  }

  // Add loading states to forms
  setupFormLoading()
}

// Setup global event listeners
function setupEventListeners() {
  // Login button
  const loginBtn = document.getElementById("loginBtn")
  if (loginBtn) {
    loginBtn.addEventListener("click", showLoginModal)
  }

  // Logout functionality
  const logoutBtn = document.getElementById("logoutBtn")
  if (logoutBtn) {
    logoutBtn.addEventListener("click", logout)
  }

  // Global error handling
  window.addEventListener("error", (e) => {
    console.error("Global error:", e.error)
    showNotification("Ha ocurrido un error inesperado", "error")
  })

  // Handle unhandled promise rejections
  window.addEventListener("unhandledrejection", (e) => {
    console.error("Unhandled promise rejection:", e.reason)
    showNotification("Error de conexión", "error")
  })
}

// Authentication functions
async function validateToken() {
  try {
    const response = await fetch("/api/auth/profile/", {
      headers: {
        Authorization: `Bearer ${authToken}`,
        "Content-Type": "application/json",
      },
    })

    if (response.ok) {
      const userData = await response.json()
      currentUser = userData
      localStorage.setItem("currentUser", JSON.stringify(userData))
      updateAuthUI()
    } else {
      // Token is invalid
      logout()
    }
  } catch (error) {
    console.error("Error validating token:", error)
    logout()
  }
}

function showLoginModal() {
  // Create login modal HTML
  const modalHTML = `
        <div class="modal fade" id="loginModal" tabindex="-1" aria-labelledby="loginModalLabel" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header bg-warning">
                        <h5 class="modal-title text-dark fw-bold" id="loginModalLabel">Iniciar Sesión</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <form id="loginForm">
                            <div class="mb-3">
                                <label for="loginEmail" class="form-label">Correo electrónico</label>
                                <input type="email" class="form-control" id="loginEmail" name="email" required>
                            </div>
                            <div class="mb-3">
                                <label for="loginPassword" class="form-label">Contraseña</label>
                                <input type="password" class="form-control" id="loginPassword" name="password" required>
                            </div>
                            <div class="d-grid">
                                <button type="submit" class="btn btn-warning">Iniciar Sesión</button>
                            </div>
                        </form>
                        <hr>
                        <div class="text-center">
                            <p class="mb-0">¿No tienes cuenta? <a href="#" id="showRegisterForm" class="text-pink">Regístrate aquí</a></p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `

  // Remove existing modal if any
  const existingModal = document.getElementById("loginModal")
  if (existingModal) {
    existingModal.remove()
  }

  // Add modal to body
  document.body.insertAdjacentHTML("beforeend", modalHTML)

  // Setup form submission
  document.getElementById("loginForm").addEventListener("submit", handleLogin)
  document.getElementById("showRegisterForm").addEventListener("click", showRegisterForm)

  // Show modal
  const modal = new window.bootstrap.Modal(document.getElementById("loginModal"))
  modal.show()
}

function showRegisterForm() {
  const modalBody = document.querySelector("#loginModal .modal-body")
  modalBody.innerHTML = `
        <form id="registerForm">
            <div class="row g-3">
                <div class="col-md-6">
                    <label for="registerFirstName" class="form-label">Nombre</label>
                    <input type="text" class="form-control" id="registerFirstName" name="first_name" required>
                </div>
                <div class="col-md-6">
                    <label for="registerLastName" class="form-label">Apellido</label>
                    <input type="text" class="form-control" id="registerLastName" name="last_name" required>
                </div>
                <div class="col-12">
                    <label for="registerUsername" class="form-label">Nombre de usuario</label>
                    <input type="text" class="form-control" id="registerUsername" name="username" required>
                </div>
                <div class="col-12">
                    <label for="registerEmail" class="form-label">Correo electrónico</label>
                    <input type="email" class="form-control" id="registerEmail" name="email" required>
                </div>
                <div class="col-md-6">
                    <label for="registerPassword" class="form-label">Contraseña</label>
                    <input type="password" class="form-control" id="registerPassword" name="password" required>
                </div>
                <div class="col-md-6">
                    <label for="registerPasswordConfirm" class="form-label">Confirmar contraseña</label>
                    <input type="password" class="form-control" id="registerPasswordConfirm" name="password_confirm" required>
                </div>
            </div>
            <div class="d-grid">
                <button type="submit" class="btn btn-warning">Registrarse</button>
            </div>
        </form>
    `

  // Setup form submission
  document.getElementById("registerForm").addEventListener("submit", handleRegister)
}

function handleLogin(event) {
  event.preventDefault()
  const email = document.getElementById("loginEmail").value
  const password = document.getElementById("loginPassword").value

  fetch("/api/auth/login/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ email, password }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.authToken) {
        localStorage.setItem("authToken", data.authToken)
        validateToken()
      } else {
        showNotification("Credenciales incorrectas", "error")
      }
    })
    .catch((error) => {
      console.error("Error logging in:", error)
      showNotification("Error de conexión", "error")
    })
}

function handleRegister(event) {
  event.preventDefault()
  const firstName = document.getElementById("registerFirstName").value
  const lastName = document.getElementById("registerLastName").value
  const username = document.getElementById("registerUsername").value
  const email = document.getElementById("registerEmail").value
  const password = document.getElementById("registerPassword").value
  const passwordConfirm = document.getElementById("registerPasswordConfirm").value

  if (password !== passwordConfirm) {
    showNotification("Las contraseñas no coinciden", "error")
    return
  }

  fetch("/api/auth/register/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ first_name: firstName, last_name: lastName, username, email, password }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.authToken) {
        localStorage.setItem("authToken", data.authToken)
        validateToken()
      } else {
        showNotification("Error al registrarse", "error")
      }
    })
    .catch((error) => {
      console.error("Error registering:", error)
      showNotification("Error de conexión", "error")
    })
}

function logout() {
  localStorage.removeItem("authToken")
  localStorage.removeItem("currentUser")
  currentUser = null
  updateAuthUI()
}

function updateAuthUI() {
  const loginBtn = document.getElementById("loginBtn")
  const logoutBtn = document.getElementById("logoutBtn")
  const registerLink = document.getElementById("showRegisterForm")

  if (currentUser) {
    loginBtn.style.display = "none"
    logoutBtn.style.display = "block"
    registerLink.style.display = "none"
  } else {
    loginBtn.style.display = "block"
    logoutBtn.style.display = "none"
    registerLink.style.display = "block"
  }
}

function showNotification(message, type) {
  const notification = document.createElement("div")
  notification.className = `alert alert-${type} alert-dismissible fade show`
  notification.role = "alert"
  notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `

  document.body.appendChild(notification)

  const alert = new window.bootstrap.Alert(notification)
  alert.close()
}

function setupFormLoading() {
  const forms = document.querySelectorAll("form")
  forms.forEach((form) => {
    form.addEventListener("submit", () => {
      form.querySelectorAll("button[type='submit']").forEach((button) => {
        button.disabled = true
        button.textContent = "Cargando..."
      })
    })
  })
}
