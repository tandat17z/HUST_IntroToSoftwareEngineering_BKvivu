  function updateTotal() {
    const stores = document.querySelectorAll('.store');

    stores.forEach((store) => {
      let storeTotal = 0;
      let remainingProducts = 0;

      const products = store.querySelectorAll('.product');
      products.forEach((product) => {
        const checkbox = product.querySelector('.checkbox');
        const priceText = product.querySelector('.price').textContent;
        const price = parseFloat(priceText.replace(' VNĐ', '').replace(',', ''));

        const quantity = parseInt(product.querySelector('.quantity-value').textContent, 10);
        const subtotalContainer = product.querySelector('.subtotal-price');

        if (!isNaN(price) && !isNaN(quantity)) {
          const subtotal = price * quantity;

          if (checkbox.checked) {
            storeTotal += subtotal;
          }

          const formattedSubtotal = `${subtotal.toLocaleString()} VNĐ`;
          subtotalContainer.textContent = formattedSubtotal;

          if (quantity > 0) {
            remainingProducts += 1;
          }
        }
      });

      const formattedStoreTotal = `${storeTotal.toLocaleString()} VNĐ`;
      store.querySelector('.store-total').textContent = `Total: ${formattedStoreTotal}`;

      if (remainingProducts === 0) {
        store.remove();
      }
    });
  }

  document.querySelectorAll('.checkbox').forEach((checkbox) => {
    checkbox.addEventListener('change', updateTotal);
  });

  document.querySelectorAll('.quantity-value').forEach((quantityValue) => {
    quantityValue.addEventListener('input', () => {
      updateSubtotalPrice(quantityValue);
      updateTotal();
    });
  });

  function updateSubtotalPrice(quantityValue) {
    const product = quantityValue.closest('.product');
    const priceText = product.querySelector('.price').textContent;
    const price = parseFloat(priceText.replace(' VNĐ', '').replace(',', ''));
    const quantity = parseInt(quantityValue.textContent, 10);
    const subtotalContainer = product.querySelector('.subtotal-price');

    if (!isNaN(price) && !isNaN(quantity)) {
      const subtotal = price * quantity;
      const formattedSubtotal = `${subtotal.toLocaleString()} VNĐ`;
      subtotalContainer.textContent = formattedSubtotal;
    }

    if (checkbox.checked && quantity === 0) {
      product.remove();
    }
  }

  function decreaseQuantity(element) {
      const itemId = element.getAttribute('data-item-id');
      const quantityValue = element.nextElementSibling;
      let quantity = parseInt(quantityValue.textContent, 10);
      if (quantity > 1) {
        quantity--;
        quantityValue.textContent = quantity;
        updateQuantity(itemId, 'decrease');
        updateTotal();
      }
    }

  function increaseQuantity(element) {
      const itemId = element.getAttribute('data-item-id');
      const quantityValue = element.previousElementSibling;
      let quantity = parseInt(quantityValue.textContent, 10);
      quantity++;
      quantityValue.textContent = quantity;
      updateQuantity(itemId, 'increase');
      updateTotal();
  }

  function removeProduct(element) {
      const itemId = element.getAttribute('data-item-id');
      const product = element.closest('.product');
      product.parentNode.removeChild(product);
      updateQuantity(itemId, 'removeitem')
      updateTotal();
  }

  function updateQuantity(itemId, action) {
    fetch('update_quantity/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            item_id: itemId,
            action: action, // 'decrease' hoặc 'increase'
        }),
    })
    .then(response => {
        // Xử lý phản hồi từ server (nếu cần)
    })
    .catch(error => {
        // Xử lý lỗi (nếu có)
    });
  }



//  Chuyển sang phần Order nè
document.addEventListener("DOMContentLoaded", function() {
  var orderForms = document.querySelectorAll('.order-form');
  orderForms.forEach(function(form) {
    form.addEventListener("submit", function(event) {
      event.preventDefault();

      // Khởi tạo mảng để lưu thông tin sản phẩm được chọn
      var selectedItems = [];

      // Lặp qua tất cả các checkbox để lấy thông tin sản phẩm được chọn
      var checkboxes = document.querySelectorAll('.checkbox');
      checkboxes.forEach(function(checkbox) {
        if (checkbox.checked) {
          var itemId = checkbox.getAttribute('data-item-id'); // Lấy id sản phẩm
          selectedItems.push(itemId); // Thêm ID sản phẩm vào mảng
        }
      });
      // Lấy CSRF token từ form
      var csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
      // Lấy id cửa hàng
      var managerId = form.querySelector('input[name="manager_id"]').value;
      // Gửi dữ liệu POST đến server (Django)
      fetch(`create_bill/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken
        },
        body: JSON.stringify({
          manager_id : managerId,
          selectedItems: selectedItems // Truyền mảng chứa thông tin sản phẩm được chọn
        })
      })
      .then(response => {
        if (response.ok) {
          return response.json();
        } else {
          throw new Error("Đặt hàng thất bại");
        }
      })
      .then(data => {
        const bill_id = data.bill_id;
        window.location.href = `payment/${bill_id}`
      })
      .catch(error => {
        // Xử lý khi có lỗi
        console.error("Lỗi khi đặt hàng:", error);
      });
    });
  });
});


// Tính giờ thanh toán
