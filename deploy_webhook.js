const express = require('express');
const nodemailer = require('nodemailer');
const { GoogleSpreadsheet } = require('google-spreadsheet');
const fs = require('fs');

// Load the webhook handler code
const webhookHandlerPath = './webhook_handler.js';
const webhookHandler = require(webhookHandlerPath);

// Fix the typo in the webhook handler
fs.readFile(webhookHandlerPath, 'utf8', (err, data) => {
  if (err) {
    console.error('Error reading webhook handler file:', err);
    return;
  }
  
  // Fix the typo: createTransporter -> createTransport
  const correctedData = data.replace(
    "const transporter = nodemailer.createTransporter(",
    "const transporter = nodemailer.createTransport("
  );
  
  fs.writeFile(webhookHandlerPath, correctedData, 'utf8', (err) => {
    if (err) {
      console.error('Error writing corrected webhook handler:', err);
      return;
    }
    console.log('Fixed typo in webhook_handler.js');
  });
});

// Install required dependencies
console.log('Installing required dependencies...');
console.log('Run the following commands to install dependencies:');
console.log('npm init -y');
console.log('npm install express nodemailer google-spreadsheet');

console.log('\nTo deploy the webhook handler:');
console.log('1. Update the email configuration in webhook_handler.js');
console.log('2. Update the Google Sheets configuration in webhook_handler.js');
console.log('3. Run: node webhook_handler.js');