const {
    verifyGooglePayToken,
    processGooglePayment,
  } = require('../helpers/googlePayHelper');
  
  const handleGooglePayPayment = async (req, res) => {
    try {
      const { paymentToken } = req.body;
  
      if (!paymentToken) {
        return res.status(400).json({ error: 'Missing paymentToken' });
      }
  
      const tokenPayload = verifyGooglePayToken(paymentToken);
  
      const paymentResult = await processGooglePayment({
        totalPrice: tokenPayload.totalPrice,
        currencyCode: tokenPayload.currencyCode,
      });
  
      return res.status(200).json({
        message: 'Payment successful',
        result: paymentResult,
      });
    } catch (err) {
      return res.status(500).json({ error: err.message });
    }
  };
  
  module.exports = {
    handleGooglePayPayment,
  };  