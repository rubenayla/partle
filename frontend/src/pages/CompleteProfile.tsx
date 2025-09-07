/**
 * @fileoverview CompleteProfile page for setting username after registration
 * @module pages/CompleteProfile
 */
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api';

/**
 * CompleteProfile Component - Username setup for new users
 * 
 * Displayed after first login when user doesn't have a username yet.
 * Username can only be set once and must be unique.
 * 
 * @returns JSX element containing the username setup form
 */
export default function CompleteProfile() {
  const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsSubmitting(true);

    try {
      await api.post('/v1/auth/set-username', { username });
      // Username set successfully, redirect to home
      navigate('/');
    } catch (err: any) {
      if (err.response?.status === 409) {
        setError('This username is already taken. Please choose another.');
      } else if (err.response?.status === 400) {
        setError(err.response.data.detail || 'Invalid username format.');
      } else {
        setError('Something went wrong. Please try again.');
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleSkip = () => {
    // Allow skipping for now, but they won't be able to add products
    navigate('/');
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900 px-4">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900 dark:text-white">
            Complete Your Profile
          </h2>
          <p className="mt-2 text-center text-sm text-gray-600 dark:text-gray-400">
            Choose a username to identify yourself on Partle
          </p>
        </div>
        
        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          <div>
            <label htmlFor="username" className="block text-sm font-medium text-gray-700 dark:text-gray-300">
              Username
            </label>
            <div className="mt-1">
              <input
                id="username"
                name="username"
                type="text"
                autoComplete="username"
                required
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="appearance-none block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-800 dark:text-white"
                placeholder="john_doe"
                pattern="[a-zA-Z0-9_-]{3,20}"
                title="3-20 characters, letters, numbers, underscore or dash only"
              />
            </div>
            <p className="mt-2 text-sm text-gray-500 dark:text-gray-400">
              3-20 characters, letters, numbers, underscore or dash only
            </p>
          </div>

          {error && (
            <div className="rounded-md bg-red-50 dark:bg-red-900/20 p-4">
              <p className="text-sm text-red-800 dark:text-red-400">{error}</p>
            </div>
          )}

          <div className="flex gap-4">
            <button
              type="submit"
              disabled={isSubmitting || username.length < 3}
              className="flex-1 flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isSubmitting ? 'Setting...' : 'Set Username'}
            </button>
            
            <button
              type="button"
              onClick={handleSkip}
              className="flex-1 flex justify-center py-2 px-4 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              Skip for now
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}