const jwt = require('jsonwebtoken');

function verifyGooglePayToken(token) {
  try {
    const payload = jwt.decode(token); 
    if (!payload) throw new Error('Invalid Google Pay token');
    return payload;
  } catch (err) {
    throw new Error(`Token verification failed: ${err.message}`);
  }
}

async function processGooglePayment(paymentInfo) {
  const { totalPrice, currencyCode } = paymentInfo;
  return {
    status: 'success',
    amount: totalPrice,
    currency: currencyCode,
    transactionId: `txn_${Math.floor(Math.random() * 1000000)}`,
  };
}

module.exports = {
  verifyGooglePayToken,
  processGooglePayment,
};