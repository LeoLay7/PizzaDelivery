  function updateQuantity(productId, change) {
    var quantitySpan = document.getElementById('quantity_' + productId);
    var currentValue = parseInt(quantitySpan.textContent);
    var newQuantity = currentValue + change;
    if (newQuantity > 0) {
      quantitySpan.textContent = newQuantity;
      var formData = new FormData(document.getElementById('quantity-form-' + productId));
      formData.append('product_id', productId);
      formData.append('quantity', newQuantity);
      formData.append('action', 'update_quantity');
      $.ajax({
        url: '/api/update_cart/',
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        success: function(response) {
          $('#amount').text(response.amount);
          console.log('Изменение прошло успешно');
        },
        error: function(xhr, status, error) {
          console.error('Request failed:', status, error);
        }
      });
    }
  }
