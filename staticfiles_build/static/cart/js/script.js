// Function to get a cookie value by name
function getCookie(name) {
    const cookies = Object.fromEntries(document.cookie.split(';').map(cookie => cookie.trim().split('=')));
    return cookies[name];
}

// Global variable for CSRF token
const csrfToken = getCookie('csrftoken');

// Function to handle adding items to the cart
function addToCart(e) {
    const button = document.getElementById("loading-button");
    button.disabled = true;
    button.classList.add("button-loader");

    const product_id = e.target.value;
    const url = "/add_to_cart";
    const data = { id: product_id };

    fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken
        },
        body: JSON.stringify(data)
    })
    .then(res => res.json())
    .then(handleCartResponse)
    .catch(handleCartError)
    .finally(() => {
        button.disabled = false;
        button.classList.remove("button-loader");
    });
}

// Function to handle successful cart response
function handleCartResponse(data) {
    console.log(data.tally);
    console.log(data.cart_items);

    document.getElementById("tally").innerHTML = data.tally;
    document.getElementById("tally2").innerHTML = data.tally;
    document.getElementById("tally-hover").innerHTML = data.tally;

    if (data.success_message) {
        const successMessageDiv = createSuccessMessage(data.success_message);
        const productArea = document.querySelector('.product-area');
        productArea.insertBefore(successMessageDiv, productArea.firstChild);
        window.scrollTo({ top: 0, behavior: 'smooth' });

        updateCartItems(data.cart_items);
    }
}

// Function to handle cart errors
function handleCartError(err) {
    console.log(err);
}

// Function to create success message div
function createSuccessMessage(message) {
    const successMessageDiv = document.createElement('div');
    successMessageDiv.classList.add('alert', 'alert-success', 'alert-dismissible', 'fade', 'show', 'mx-5', 'my-1');
    successMessageDiv.setAttribute('role', 'alert');
    successMessageDiv.innerHTML = `
        <strong>Success!</strong> ${message}
        <button type="button" class="close" data-dismiss="alert" aria-label="Close">
            <span aria-hidden="true">&times;</span>
        </button>
    `;
    return successMessageDiv;
}

// Function to update cart items
function updateCartItems(cartItems) {
    const shoppingList = document.querySelector(".shopping-list");
    shoppingList.innerHTML = "";
    let totalAmount = 0;

    cartItems.forEach(cartItem => {
        fetch(`api/v1/photos/${cartItem.photo_id}`)
            .then(response => response.json())
            .then(photo => {
                const listItem = createCartItemElement(cartItem, photo);
                shoppingList.appendChild(listItem);
                const subTotal = parseInt(cartItem.quantity) * parseInt(photo.price);
                totalAmount += subTotal;
                updateTotalAmount(totalAmount);
            })
            .catch(error => console.error('Error fetching photo:', error));
    });
}

// Function to create cart item element
function createCartItemElement(cartItem, photo) {
    const listItem = document.createElement("li");
    listItem.innerHTML = `
        <a href="#" class="remove" title="Remove this item"><i class="fa fa-remove"></i></a>
        <a class="cart-img" href="#"><img src="${photo.webp_image}" style="width: 70px; height: auto" alt="${photo.title}"></a>
        <h4><a href="#">${photo.title}</a></h4>
        <p class="quantity">${cartItem.quantity}x - <span class="amount">Sh. ${photo.price}</span></p>
    `;
    return listItem;
}

// Function to update total amount
function updateTotalAmount(totalAmount) {
    const totalAmountElement = document.querySelector(".total-amount");
    if (totalAmountElement) {
        totalAmountElement.textContent = `Sh. ${Number(totalAmount).toFixed(1)}`;
    }
}

// Event listener for add to cart buttons
document.querySelectorAll(".product-action-2 button").forEach(btn => {
    btn.addEventListener("click", addToCart);
});



