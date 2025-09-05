export default {
  async fetch(request, env, ctx) {
    // Only allow POST requests
    if (request.method !== 'POST') {
      return new Response('Method not allowed', { status: 405 });
    }

    try {
      // Parse the incoming request
      const { to_email, token, api_key } = await request.json();
      
      // Simple API key validation
      if (api_key !== env.API_KEY) {
        return new Response('Unauthorized', { status: 401 });
      }

      // Validate required fields
      if (!to_email || !token) {
        return new Response('Missing required fields', { status: 400 });
      }

      // Check if Resend API key is configured
      if (!env.RESEND_API_KEY) {
        return new Response(JSON.stringify({
          status: "error",
          message: "Resend API key not configured",
          instructions: "1. Sign up at https://resend.com (free)\n2. Add your domain\n3. Get API key\n4. Add RESEND_API_KEY to Worker environment variables"
        }), {
          status: 500,
          headers: { "Content-Type": "application/json" }
        });
      }

      // Create the password reset email
      const resetLink = `https://partle.rubenayla.xyz/reset-password?token=${token}`;
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

      // Send email using Resend API
      const resendResponse = await fetch("https://api.resend.com/emails", {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${env.RESEND_API_KEY}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          from: "Partle <noreply@rubenayla.xyz>",
          to: [to_email],
          subject: "Reset your Partle password",
          text: emailContent
        })
      });

      const result = await resendResponse.json();

      // Check if email was sent successfully
      if (resendResponse.ok) {
        return new Response(JSON.stringify({ 
          status: "ok", 
          message: "Email sent successfully",
          id: result.id
        }), {
          status: 200,
          headers: { "Content-Type": "application/json" }
        });
      } else {
        console.error('Resend error:', resendResponse.status, result);
        
        return new Response(JSON.stringify({ 
          status: "error", 
          message: "Failed to send email",
          details: result
        }), {
          status: 500,
          headers: { "Content-Type": "application/json" }
        });
      }

    } catch (error) {
      console.error('Email sending error:', error);
      return new Response(JSON.stringify({ 
        status: "error", 
        message: "Failed to send email",
        error: error.message 
      }), {
        status: 500,
        headers: { "Content-Type": "application/json" }
      });
    }
  }
};