import React, { useState, useEffect } from 'react';
import { currentUser, changePassword } from '../api/auth';

export default function Account() {
  const [email, setEmail] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmNewPassword, setConfirmNewPassword] = useState('');
  const [message, setMessage] = useState('');

  useEffect(() => {
    const fetchUserEmail = async () => {
      try {
        const user = await currentUser();
        setEmail(user.email);
      } catch (err) {
        setError('Failed to fetch user email.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchUserEmail();
  }, []);

  const handleChangePassword = async (e) => {
    e.preventDefault();
    setMessage('');
    setError(null);

    if (newPassword !== confirmNewPassword) {
      setError('New passwords do not match.');
      return;
    }

    try {
      await changePassword(currentPassword, newPassword);
      setMessage('Password changed successfully!');
      setCurrentPassword('');
      setNewPassword('');
      setConfirmNewPassword('');
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to change password.');
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen w-screen flex flex-col items-center justify-center bg-background text-foreground p-8">
        <p>Loading account details...</p>
      </div>
    );
  }

  if (error && !message) {
    return (
      <div className="min-h-screen w-screen flex flex-col items-center justify-center bg-background text-foreground p-8">
        <p className="text-red-500">{error}</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen w-screen flex flex-col items-center justify-center bg-background text-foreground p-8">
      <div className="p-8 bg-surface rounded-xl shadow-lg text-center">
        <h1 className="text-3xl font-bold mb-4">Account Details</h1>
        <p className="text-lg mb-4">Logged in as: <span className="font-semibold">{email}</span></p>

        <h2 className="text-2xl font-bold mb-4">Change Password</h2>
        <form onSubmit={handleChangePassword} className="space-y-4">
          <div>
            <label htmlFor="current-password" className="block text-left text-sm font-medium text-foreground">Current Password</label>
            <input
              type="password"
              id="current-password"
              className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary sm:text-sm bg-background text-foreground"
              value={currentPassword}
              onChange={(e) => setCurrentPassword(e.target.value)}
              required
            />
          </div>
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
          {message && <p className="text-green-500 text-sm">{message}</p>}
          {error && <p className="text-red-500 text-sm">{error}</p>}
          <button
            type="submit"
            className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary hover:bg-primary-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
          >
            Change Password
          </button>
        </form>
      </div>
    </div>
  );
}
