const API_URL = "http://127.0.0.1:8000";

let accessToken = sessionStorage.getItem("access_token");

const booksContainer = document.getElementById("books-container");
const catalogMessage = document.getElementById("catalog-message");
const accountMessage = document.getElementById("account-message");
const reservationsContainer = document.getElementById("reservations-container");
const reservationsMessage = document.getElementById("reservations-message");
const purchasesContainer = document.getElementById("purchases-container");
const purchasesMessage = document.getElementById("purchases-message");

const bookDetails = document.getElementById("book-details");
const reviewsContainer = document.getElementById("reviews-container");
const reviewsMessage = document.getElementById("reviews-message");
const reviewFormContainer = document.getElementById("review-form-container");

let selectedBookId = null;

function showMessage(element, message, type = "") {
    element.textContent = message;
    element.className = `message ${type}`.trim();
}

async function apiRequest(path, options = {}) {
    const headers = new Headers(options.headers || {});

    if (options.body && !(options.body instanceof FormData)) {
        headers.set("Content-Type", "application/json");
    }

    if (accessToken) {
        headers.set("Authorization", `Bearer ${accessToken}`);
    }

    const response = await fetch(`${API_URL}${path}`, {
        ...options,
        headers
    });

    const contentType = response.headers.get("content-type") || "";
    const data = contentType.includes("application/json")
        ? await response.json()
        : await response.text();

    if (!response.ok) {
        const detail = typeof data === "object" && data !== null
            ? data.detail
            : null;

        throw new Error(detail || `Fout: HTTP ${response.status}`);
    }

    return data;
}

async function loadBooks() {
    showMessage(catalogMessage, "Boeken laden...");

    try {
        const books = await apiRequest("/books/");
        booksContainer.replaceChildren();

        if (books.length === 0) {
            showMessage(catalogMessage, "Er zijn momenteel geen boeken beschikbaar.");
            return;
        }

        showMessage(catalogMessage, `${books.length} boek(en) gevonden.`, "success");

        books.forEach(book => {
            const card = document.createElement("article");
            card.className = "book-card";

            const cover = document.createElement("div");
            cover.className = "book-cover";
            cover.textContent = "📚";
            cover.setAttribute("aria-hidden", "true");

            const title = document.createElement("h3");
            title.textContent = book.title;
            title.tabIndex = 0;
            title.setAttribute("role", "button");
            title.setAttribute("aria-label", `Bekijk details van ${book.title}`);

            title.style.cursor = "pointer";

            title.addEventListener("click", () => openBookDetails(book));

            title.addEventListener("keydown", event => {
    if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        openBookDetails(book);
    }
});
            const author = document.createElement("p");
            author.className = "book-author";
            author.textContent = `Door ${book.author}`;

            const description = document.createElement("p");
            description.className = "book-description";
            description.textContent = book.description || "Geen beschrijving beschikbaar.";

            const price = document.createElement("p");
            price.className = "book-price";
            price.textContent = `€ ${Number(book.price).toFixed(2)}`;

            const stock = document.createElement("p");
            stock.className = "book-stock";
            stock.textContent = `Voorraad: ${book.stock}`;

            const reserveButton = document.createElement("button");
            reserveButton.className = "button";
            reserveButton.textContent = "Reserveer dit boek";
            reserveButton.disabled = book.stock <= 0;

            if (book.stock <= 0) {
                reserveButton.textContent = "Niet op voorraad";
            }

            reserveButton.addEventListener("click", () => reserveBook(book.id));

            card.append(cover, title, author, description, price, stock, reserveButton);
            booksContainer.appendChild(card);
        });
    } catch (error) {
        showMessage(
            catalogMessage,
            `De catalogus kon niet worden geladen: ${error.message}`,
            "error"
        );
    }
}

async function registerUser(event) {
    event.preventDefault();

    const form = event.currentTarget;
    const formData = new FormData(form);

    const userData = {
        username: formData.get("username").trim(),
        email: formData.get("email").trim(),
        password: formData.get("password")
    };

    try {
        await apiRequest("/users/register", {
            method: "POST",
            body: JSON.stringify(userData)
        });

        form.reset();

        showMessage(
            accountMessage,
            "Account aangemaakt. Je kunt nu inloggen.",
            "success"
        );
    } catch (error) {
        showMessage(accountMessage, error.message, "error");
    }
}

async function loginUser(event) {
    event.preventDefault();
    await loadPurchases();
    await loadReservations();
    const form = event.currentTarget;
    const formData = new FormData(form);

    const loginData = new URLSearchParams();
    loginData.set("username", formData.get("username"));
    loginData.set("password", formData.get("password"));

    try {
        const response = await apiRequest("/users/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: loginData
        });

        accessToken = response.access_token;
        sessionStorage.setItem("access_token", accessToken);

        form.reset();

        showMessage(accountMessage, "Je bent ingelogd.", "success");

        updateLoginState();
        await loadReservations();
    } catch (error) {
        showMessage(accountMessage, error.message, "error");
    }
}

function logoutUser() {
    accessToken = null;
    sessionStorage.removeItem("access_token");

    reservationsContainer.replaceChildren();
    showMessage(reservationsMessage, "");
    showMessage(accountMessage, "Je bent uitgelogd.", "success");

    updateLoginState();
}

function updateLoginState() {
    const loggedIn = Boolean(accessToken);

    document.getElementById("logout-button")
        .classList.toggle("hidden", !loggedIn);

    document.getElementById("my-reservations")
        .classList.toggle("hidden", !loggedIn);

    document.querySelectorAll(".book-card .button").forEach(button => {
        button.disabled = !loggedIn || button.textContent === "Niet op voorraad";
    });
    document.getElementById("my-purchases")
        .classList.toggle("hidden", !loggedIn);
}

async function reserveBook(bookId) {
    if (!accessToken) {
        showMessage(
            accountMessage,
            "Log eerst in voordat je een boek reserveert.",
            "error"
        );

        document.getElementById("account").scrollIntoView({
            behavior: "smooth"
        });

        return;
    }

    try {
        await apiRequest("/reservations/", {
            method: "POST",
            body: JSON.stringify({
                book_id: bookId,
                quantity: 1
            })
        });

        showMessage(
            reservationsMessage,
            "Boek succesvol gereserveerd.",
            "success"
        );

        await loadBooks();
        await loadReservations();
    } catch (error) {
        showMessage(reservationsMessage, error.message, "error");
    }
}

async function loadReservations() {
    if (!accessToken) {
        return;
    }

    showMessage(reservationsMessage, "Reserveringen laden...");

    try {
        const reservations = await apiRequest("/reservations/");
        reservationsContainer.replaceChildren();

        if (reservations.length === 0) {
            showMessage(reservationsMessage, "Je hebt nog geen reserveringen.");
            return;
        }

        showMessage(
            reservationsMessage,
            `${reservations.length} reservering(en) gevonden.`,
            "success"
        );

        reservations.forEach(reservation => {
            const item = document.createElement("article");
            item.className = "reservation-item";

            const title = document.createElement("h3");
            title.textContent = `Reservering #${reservation.id}`;

            const details = document.createElement("p");
            details.textContent =
                `Boek-ID: ${reservation.book_id} · Aantal: ${reservation.quantity}`;

            const status = document.createElement("p");
            status.textContent = `Status: ${reservation.status}`;

            item.append(title, details, status);
            reservationsContainer.appendChild(item);
        });
    } catch (error) {
        if (error.message.includes("token") || error.message.includes("Token")) {
            logoutUser();
            showMessage(
                accountMessage,
                "Je sessie is ongeldig. Log opnieuw in.",
                "error"
            );
            return;
        }

        showMessage(reservationsMessage, error.message, "error");
    }
}

document.getElementById("register-form")
    .addEventListener("submit", registerUser);

document.getElementById("login-form")
    .addEventListener("submit", loginUser);

document.getElementById("logout-button")
    .addEventListener("click", logoutUser);

document.getElementById("refresh-books")
    .addEventListener("click", loadBooks);

updateLoginState();
loadBooks();

if (accessToken) {
    loadReservations();
}
async function loadPurchases() {
    if (!accessToken) {
        return;
    }

    showMessage(purchasesMessage, "Gekochte boeken laden...");

    try {
        const purchases = await apiRequest("/purchases/me");

        purchasesContainer.replaceChildren();

        if (purchases.length === 0) {
            showMessage(
                purchasesMessage,
                "Je hebt nog geen boeken gekocht."
            );
            return;
        }

        showMessage(
            purchasesMessage,
            `${purchases.length} aankoop/aankopen gevonden.`,
            "success"
        );

        purchases.forEach(purchase => {
            const card = document.createElement("article");
            card.className = "book-card";

            const title = document.createElement("h3");
            title.textContent = purchase.title;

            const author = document.createElement("p");
            author.className = "book-author";
            author.textContent = `Door ${purchase.author}`;

            const reviewButton = document.createElement("button");
            reviewButton.className = "button";
            reviewButton.textContent = "Schrijf een review";

            reviewButton.addEventListener("click", () => {
                document.getElementById("catalogus").scrollIntoView({
                    behavior: "smooth"
                });

                showMessage(
                    catalogMessage,
                    `Zoek boek-ID ${purchase.book_id} in de catalogus om de review te schrijven.`
                );
            });

            card.append(title, author, reviewButton);
            purchasesContainer.appendChild(card);
        });
    } catch (error) {
        showMessage(purchasesMessage, error.message, "error");
    }
}
if (accessToken) {
    loadPurchases();
}
async function openBookDetails(book) {
    selectedBookId = book.id;

    document.getElementById("detail-title").textContent = book.title;
    document.getElementById("detail-author").textContent =
        `Door ${book.author}`;
    document.getElementById("detail-description").textContent =
        book.description || "Geen beschrijving beschikbaar.";

    bookDetails.classList.remove("hidden");

    reviewFormContainer.classList.toggle("hidden", !accessToken);

    bookDetails.scrollIntoView({ behavior: "smooth" });

    await loadReviews(book.id);
}

async function loadReviews(bookId) {
    showMessage(reviewsMessage, "Reviews laden...");
    reviewsContainer.replaceChildren();

    try {
        const reviews = await apiRequest(`/reviews/book/${bookId}`);

        if (reviews.length === 0) {
            showMessage(reviewsMessage, "Er zijn nog geen reviews.");
            return;
        }

        showMessage(reviewsMessage, `${reviews.length} review(s) gevonden.`);

        reviews.forEach(review => {
            const card = document.createElement("article");
            card.className = "review-card";

            const score = document.createElement("p");
            score.className = "review-score";
            score.textContent = `${review.score}/5 sterren`;

            const text = document.createElement("p");
            text.textContent = review.text;

            card.append(score, text);
            reviewsContainer.appendChild(card);
        });
    } catch (error) {
        showMessage(reviewsMessage, error.message, "error");
    }
}

async function submitReview(event) {
    event.preventDefault();

    if (!accessToken || !selectedBookId) {
        showMessage(
            reviewsMessage,
            "Log in en selecteer een boek voordat je een review schrijft.",
            "error"
        );
        return;
    }

    const formData = new FormData(event.currentTarget);

    const reviewData = {
        book_id: selectedBookId,
        score: Number(formData.get("score")),
        text: formData.get("text").trim()
    };

    try {
        await apiRequest("/reviews/", {
            method: "POST",
            body: JSON.stringify(reviewData)
        });

        event.currentTarget.reset();

        showMessage(
            reviewsMessage,
            "Je review is succesvol geplaatst.",
            "success"
        );

        await loadReviews(selectedBookId);
    } catch (error) {
        showMessage(reviewsMessage, error.message, "error");
    }
}

document.getElementById("review-form")
    .addEventListener("submit", submitReview);