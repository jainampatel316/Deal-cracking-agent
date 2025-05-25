// Webhook endpoint to handle post-call actions
const express = require('express');
const nodemailer = require('nodemailer');
const { GoogleSpreadsheet } = require('google-spreadsheet');

const app = express();
app.use(express.json());

// Email configuration
const transporter = nodemailer.createTransporter({
  service: 'gmail',
  auth: {
    user: 'your-email@gmail.com',
    pass: 'your-app-password'
  }
});

// Google Sheets configuration
const doc = new GoogleSpreadsheet('your-sheet-id');

app.post('/omnidimension-webhook', async (req, res) => {
  try {
    const { callData, resellers, topDeals, userEmail } = req.body;
    
    // Send email with top 3 deals
    await sendDealsEmail(userEmail, topDeals);
    
    // Log to Google Sheets
    await logToGoogleSheets(callData, resellers);
    
    res.status(200).json({ success: true });
  } catch (error) {
    console.error('Webhook error:', error);
    res.status(500).json({ error: 'Webhook processing failed' });
  }
});

async function sendDealsEmail(userEmail, topDeals) {
  const emailHTML = `
    <h2>🔥 Your Top 3 Sneaker Deals</h2>
    <p>Here are the best offers we found for you:</p>
    
    ${topDeals.map((deal, index) => `
      <div style="border: 1px solid #ddd; padding: 15px; margin: 10px 0;">
        <h3>#${index + 1} - ${deal.reseller}</h3>
        <p><strong>Price:</strong> $${deal.price}</p>
        <p><strong>Delivery:</strong> ${deal.delivery_days} days</p>
        <p><strong>Condition:</strong> ${deal.condition}</p>
        <p><strong>Authenticity:</strong> ${deal.authenticity_guarantee ? '✅ Guaranteed' : '❌ Not guaranteed'}</p>
        <p><strong>Value Score:</strong> ${deal.value_score}/100</p>
      </div>
    `).join('')}
    
    <p>Contact your preferred seller directly or reply to this email for assistance!</p>
  `;
  
  await transporter.sendMail({
    from: 'your-email@gmail.com',
    to: userEmail,
    subject: '🔥 Your Top 3 Sneaker Deals - Ready to Buy!',
    html: emailHTML
  });
}

async function logToGoogleSheets(callData, resellers) {
  await doc.useServiceAccountAuth({
    client_email: 'your-service-account@project.iam.gserviceaccount.com',
    private_key: 'your-private-key'
  });
  
  await doc.loadInfo();
  const sheet = doc.sheetsByIndex[0];
  
  // Log each reseller interaction
  for (const reseller of resellers) {
    await sheet.addRow({
      'Timestamp': new Date().toISOString(),
      'Call ID': callData.call_id,
      'User Email': callData.user_email,
      'Product': callData.product,
      'Reseller Name': reseller.name,
      'Original Price': reseller.original_price,
      'Negotiated Price': reseller.final_price,
      'Delivery Days': reseller.delivery_days,
      'Authenticity Guarantee': reseller.authenticity_guarantee,
      'Call Duration': reseller.call_duration,
      'Success': reseller.call_successful
    });
  }
}

app.listen(3000, () => {
  console.log('Webhook server running on port 3000');
});