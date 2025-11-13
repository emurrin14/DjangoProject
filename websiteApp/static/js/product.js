document.addEventListener("DOMContentLoaded", function () {
    const sizeButtons = document.querySelectorAll(".productSizeButtons");
    const selectedVariantInput = document.getElementById("selectedVariantId");
    const addToCartForm = document.getElementById("addToCartForm");
    const addToCartBtn = document.getElementById("addToCartBtn");
    const cartStatus = document.getElementById("cartStatus");
  
    // --- SIZE SELECTION ---
    sizeButtons.forEach((button) => {
      button.addEventListener("click", () => {
        // Remove active styling from all buttons
        sizeButtons.forEach((btn) => btn.classList.remove("active-size"));
        // Add active styling to the clicked one
        button.classList.add("active-size");
  
        // Set selected variant ID
        const variantId = button.dataset.variantId;
        selectedVariantInput.value = variantId;
  
        // Enable the "Add to Cart" button
        addToCartBtn.disabled = false;
      });
    });
  
    // --- FORM SUBMIT (AJAX) ---
    addToCartForm.addEventListener("submit", function (event) {
      event.preventDefault(); // prevent normal form submission
  
      const formData = new FormData(addToCartForm);
      const url = addToCartForm.action;
  
      // Get CSRF token
      const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  
      fetch(url, {
        method: "POST",
        headers: {
          "X-CSRFToken": csrftoken,
        },
        body: formData,
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error("Network response was not ok");
          }
          return response.json();
        })
        .then((data) => {
          if (data.success) {
            cartStatus.innerHTML = `<p style="color: green;">Added to cart! Quantity: ${data.quantity}</p>`;
          } else {
            cartStatus.innerHTML = `<p style="color: red;">Error adding to cart.</p>`;
          }
        })
        .catch((error) => {
          console.error("Error:", error);
          cartStatus.innerHTML = `<p style="color: red;">Something went wrong.</p>`;
        });
    });
  });
  