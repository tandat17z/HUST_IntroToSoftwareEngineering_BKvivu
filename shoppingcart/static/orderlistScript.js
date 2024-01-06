// Thanh toán đơn hàng
function payOrder(bill_id){
    const paymentUrl = `/shoppingcart/payment/${bill_id}/`;
    const absolutePaymentUrl = window.location.origin + paymentUrl;
    window.location.href = absolutePaymentUrl;
}
// Hủy đơn hàng
function cancelOrder(bill_id){
    const cancelOrderUrl = `/shoppingcart/cancelpayment/${bill_id}/`;
    const absolutePaymentUrl = window.location.origin + cancelOrderUrl;
    window.location.href = absolutePaymentUrl;
}