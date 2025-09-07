/**
 * @fileoverview Account page component for user account management
 * @module pages/Account
 */
import React, { useState, useEffect } from 'react';
import { currentUser, changePassword } from '../api/auth';
import { User } from '../types';

/**
 * Account Component - User account management page
 * 
 * Displays user account information and provides password change functionality.
 * Requires user authentication to access.
 * 
 * Features:
 * - Display current user email
 * - Change password form with validation
 * - Loading states and error handling
 * - Success/error message display
 * 
 * @returns JSX element containing the account management interface
 * 
 * @example
 * ```tsx
 * // Used in routing
 * <Route 
 *   path="/account" 
 *   element={
 *     <RequireAuth>
 *       <Account />
 *     </RequireAuth>
 *   } 
 * />
 * ```
 */
export default function Account() {
  const [email, setEmail] = useState<string>('');
  const [username, setUsername] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [currentPassword, setCurrentPassword] = useState<string>('');
  const [newPassword, setNewPassword] = useState<string>('');
  const [confirmNewPassword, setConfirmNewPassword] = useState<string>('');
  const [message, setMessage] = useState<string>('');

  useEffect(() => {
    /**
     * Fetch current user's information
     */
    const fetchUserInfo = async (): Promise<void> => {
      try {
        const user: User = await currentUser();
        setEmail(user.email);
        setUsername(user.username || null);
      } catch (err: any) {
        setError('Failed to fetch user information.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchUserInfo();
  }, []);

  /**
   * Handle password change form submission
   * 
   * @param e - Form submission event
   */
  const handleChangePassword = async (e: React.FormEvent): Promise<void> => {
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
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to change password.');
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen w-screen flex flex-col items-center justify-center bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-white p-8">
        <p className="text-gray-600 dark:text-gray-400">Loading account details...</p>
      </div>
    );
  }

  if (error && !message) {
    return (
      <div className="min-h-screen w-screen flex flex-col items-center justify-center bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-white p-8">
        <p className="text-red-500 dark:text-red-400">{error}</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen w-screen flex flex-col items-center justify-center bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-white p-8">
      <div className="p-8 bg-white dark:bg-gray-800 rounded-xl shadow-lg text-center border border-gray-200 dark:border-gray-700">
        <h1 className="text-3xl font-bold mb-4">Account Details</h1>
        {username && (
          <p className="text-xl mb-2">
            Username: <span className="font-semibold text-blue-600 dark:text-blue-400">@{username}</span>
          </p>
        )}
        <p className="text-lg mb-4">
          Email: <span className="font-semibold">{email}</span>
        </p>
        {!username && (
          <div className="mb-4 p-3 bg-yellow-100 dark:bg-yellow-900/20 rounded-lg">
            <p className="text-sm text-yellow-800 dark:text-yellow-400">
              You haven't set a username yet. 
              <a href="/complete-profile" className="ml-1 underline hover:text-yellow-900 dark:hover:text-yellow-300">
                Set your username
              </a>
            </p>
          </div>
        )}

        <h2 className="text-2xl font-bold mb-4">Change Password</h2>
        <form onSubmit={handleChangePassword} className="space-y-4">
          <div>
            <label htmlFor="current-password" className="block text-left text-sm font-medium text-gray-700 dark:text-gray-300">
              Current Password
            </label>
            <input
              type="password"
              id="current-password"
              className="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
              value={currentPassword}
              onChange={(e) => setCurrentPassword(e.target.value)}
              required
            />
          </div>
          <div>
            <label htmlFor="new-password" className="block text-left text-sm font-medium text-gray-700 dark:text-gray-300">
              New Password
            </label>
            <input
              type="password"
              id="new-password"
              className="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
              required
            />
          </div>
          <div>
            <label htmlFor="confirm-new-password" className="block text-left text-sm font-medium text-gray-700 dark:text-gray-300">
              Confirm New Password
            </label>
            <input
              type="password"
              id="confirm-new-password"
              className="mt-1 block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
              value={confirmNewPassword}
              onChange={(e) => setConfirmNewPassword(e.target.value)}
              required
            />
          </div>
          {message && <p className="text-green-500 text-sm">{message}</p>}
          {error && <p className="text-red-500 text-sm">{error}</p>}
          <button
            type="submit"
            className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            Change Password
          </button>
        </form>
      </div>
    </div>
  );
}
