function deleteProduct(productId) {
  var form = document.getElementById('delete-form-' + productId);
  var formData = new FormData(form);

  formData.append('action', 'delete product');
  formData.append('product_id', productId);
  $.ajax({
    url: '/api/update_cart/',
    type: 'POST',
    data: formData,
    processData: false,
    contentType: false,
    success: function(response) {
      $('#product_' + productId).remove();
      $('#amount').text(response.amount);
      console.log('Продукт успешно удален из корзины');
    },
    error: function(xhr, status, error) {
      console.error('Request failed:', status, error);
    }
  });
}
