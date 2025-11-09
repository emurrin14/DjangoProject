document.addEventListener("DOMContentLoaded", () => {
  const sizeButtons = document.querySelectorAll(".productSizeButtons");
  const hiddenInput = document.querySelector("#selectedVariantId");
  const addToCartBtn = document.querySelector("#addToCartBtn");
  const statusDiv = document.querySelector("#cartStatus");

  // Handle size selection
  sizeButtons.forEach(btn => {
    btn.addEventListener("click", () => {
      // Remove active highlight from others
      sizeButtons.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");

      // Store selected variant ID
      const variantId = btn.dataset.variantId;
      hiddenInput.value = variantId;
      addToCartBtn.disabled = false;
    });
  });

  // Handle AJAX Add to Cart
  addToCartBtn.addEventListener("click", () => {
    const variantId = hiddenInput.value;
    if (!variantId) return;

    fetch("{% url 'add_to_cart' %}", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),  // Django CSRF helper below
      },
      body: JSON.stringify({
        variant_id: variantId,
        quantity: 1,
      }),
    })
    .then(response => response.json())
    .then(data => {
      statusDiv.textContent = data.message || "Added to cart!";
      statusDiv.style.color = "green";
    })
    .catch(err => {
      statusDiv.textContent = "Error adding to cart.";
      statusDiv.style.color = "red";
      console.error(err);
    });
  });

  // Helper to get CSRF token from cookies
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let cookie of cookies) {
        cookie = cookie.trim();
        if (cookie.startsWith(name + "=")) {
          cookieValue = decodeURIComponent(cookie.slice(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
});