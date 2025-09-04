export default {
  async fetch(request, env, ctx) {
    // Only allow POST requests
    if (request.method !== 'POST') {
      return new Response('Method not allowed', { status: 405 });
    }

    try {
      // Parse the incoming request
      const { to_email, token, api_key } = await request.json();
      
      // Simple API key validation (you'll set this in environment variables)
      if (api_key !== env.API_KEY) {
        return new Response('Unauthorized', { status: 401 });
      }

      // Validate required fields
      if (!to_email || !token) {
        return new Response('Missing required fields', { status: 400 });
      }

      // Create the password reset email
      const resetLink = `https://partle.com/reset-password?token=${token}`;
      const emailContent = `
Hello,

You requested a password reset for your Partle account.

Click the link below to reset your password:
${resetLink}

This link will expire in 1 hour.

If you didn't request this reset, you can safely ignore this email.

Best regards,
Partle Team
`;

      // Send the email using Cloudflare's email API
      const message = {
        from: { email: "noreply@rubenayla.xyz", name: "Partle" },
        to: [{ email: to_email }],
        subject: "Reset your Partle password",
        content: [{
          type: "text/plain",
          value: emailContent
        }]
      };

      // Use Cloudflare's email sending capability
      await fetch("https://api.cloudflare.com/client/v4/accounts/" + env.ACCOUNT_ID + "/email/routing/addresses/noreply@rubenayla.xyz/message", {
        method: "POST",
        headers: {
          "Authorization": "Bearer " + env.EMAIL_API_TOKEN,
          "Content-Type": "application/json"
        },
        body: JSON.stringify(message)
      });

      return new Response(JSON.stringify({ status: "ok", message: "Email sent successfully" }), {
        status: 200,
        headers: { "Content-Type": "application/json" }
      });

    } catch (error) {
      console.error('Email sending error:', error);
      return new Response(JSON.stringify({ status: "error", message: "Failed to send email" }), {
        status: 500,
        headers: { "Content-Type": "application/json" }
      });
    }
  }
};