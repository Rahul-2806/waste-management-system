const express = require('express');
const nodemailer = require('nodemailer');
const cors = require('cors');
require('dotenv').config();

const app = express();
app.use(express.json());
app.use(cors()); // Enable CORS to allow frontend requests

// In-memory storage for OTPs (use a database like Redis in production)
const otps = new Map();

// Nodemailer configuration (using Gmail as an example)
const transporter = nodemailer.createTransport({
    service: 'gmail',
    auth: {
        user: process.env.EMAIL_USER, // Your Gmail address
        pass: process.env.EMAIL_PASS, // Your Gmail App Password (not regular password)
    },
});

// Generate a 6-digit OTP
function generateOTP() {
    return Math.floor(100000 + Math.random() * 900000).toString();
}

// Send OTP endpoint
app.post('/send-otp', async (req, res) => {
    const { email } = req.body;

    if (!email) {
        return res.status(400).json({ success: false, message: 'Email is required' });
    }

    const otp = generateOTP();
    otps.set(email, otp); // Store OTP temporarily

    const mailOptions = {
        from: process.env.EMAIL_USER,
        to: email,
        subject: 'Your OTP for Registration',
        text: `Your One-Time Password (OTP) is: ${otp}\n\nThis code expires in 5 minutes.`,
    };

    try {
        await transporter.sendMail(mailOptions);
        console.log(`OTP ${otp} sent to ${email}`);
        res.json({ success: true, message: 'OTP sent successfully' });
    } catch (error) {
        console.error('Error sending email:', error);
        res.status(500).json({ success: false, message: 'Failed to send OTP' });
    }
});

// Verify OTP endpoint
app.post('/verify-otp', (req, res) => {
    const { email, otp } = req.body;

    if (!email || !otp) {
        return res.status(400).json({ success: false, message: 'Email and OTP are required' });
    }

    const storedOtp = otps.get(email);

    if (!storedOtp) {
        return res.status(400).json({ success: false, message: 'No OTP found for this email' });
    }

    if (storedOtp === otp) {
        otps.delete(email); // Clear OTP after successful verification
        res.json({ success: true, message: 'OTP verified successfully' });
    } else {
        res.json({ success: false, message: 'Invalid OTP' });
    }
});

// Register user endpoint (placeholder)
app.post('/register', (req, res) => {
    const { name, address, phone, email, password, gender } = req.body;
    // Add logic to save user data to a database here
    console.log('User registered:', { name, address, phone, email, password, gender });
    res.json({ success: true, message: 'Registration successful' });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});