import React, { useState, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import api from '../api';

export default function ResetPassword() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const [newPassword, setNewPassword] = useState('');
  const [confirmNewPassword, setConfirmNewPassword] = useState('');
  const [message, setMessage] = useState('');
  const [error, setError] = useState(null);
  const [token, setToken] = useState(null);

  useEffect(() => {
    const tokenFromUrl = searchParams.get('token');
    if (tokenFromUrl) {
      setToken(tokenFromUrl);
    } else {
      setError('No reset token found in URL.');
    }
  }, [searchParams]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage('');
    setError(null);

    if (!token) {
      setError('Missing reset token.');
      return;
    }

    if (newPassword !== confirmNewPassword) {
      setError('New passwords do not match.');
      return;
    }

    try {
      await api.post('/v1/auth/reset-password', { token, new_password: newPassword });
      setMessage('Your password has been reset successfully. You can now log in with your new password.');
      setNewPassword('');
      setConfirmNewPassword('');
      // Optionally redirect to login page after a delay
      setTimeout(() => navigate('/'), 3000);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to reset password. The token might be invalid or expired.');
    }
  };

  return (
    <div className="min-h-screen w-screen flex flex-col items-center justify-center bg-background text-foreground p-8">
      <div className="p-8 bg-surface rounded-xl shadow-lg text-center">
        <h1 className="text-3xl font-bold mb-4">Reset Password</h1>
        {!token && !error ? (
          <p>Loading...</p>
        ) : (
          <form onSubmit={handleSubmit} className="space-y-4">
            {error && <p className="text-red-500 text-sm">{error}</p>}
            {message && <p className="text-green-500 text-sm">{message}</p>}

            <div>
              <label htmlFor="new-password" className="block text-left text-sm font-medium text-foreground">New Password</label>
              <input
                type="password"
                id="new-password"
                className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm bg-background text-foreground"
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
                required
              />
            </div>
            <div>
              <label htmlFor="confirm-new-password" className="block text-left text-sm font-medium text-foreground">Confirm New Password</label>
              <input
                type="password"
                id="confirm-new-password"
                className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm bg-background text-foreground"
                value={confirmNewPassword}
                onChange={(e) => setConfirmNewPassword(e.target.value)}
                required
              />
            </div>
            <button
              type="submit"
              className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
            >
              Reset Password
            </button>
          </form>
        )}
      </div>
    </div>
  );
}
