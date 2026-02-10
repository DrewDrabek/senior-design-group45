'use client';

import { useAuth0 } from "@auth0/auth0-react";

export default function Home() {
  const { isLoading, isAuthenticated, loginWithRedirect, logout, user } = useAuth0();

  // 1. Loading State (Prevents flickering)
  if (isLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-zinc-50 dark:bg-black">
        <div className="text-xl font-semibold text-zinc-600 dark:text-zinc-400">Loading...</div>
      </div>
    );
  }

  // 2. LOGGED OUT STATE: Show the "Login Screen" (Landing Page)
  if (!isAuthenticated) {
    return (
      <div className="flex min-h-screen flex-col items-center justify-center bg-zinc-50 dark:bg-black p-6">
        <div className="max-w-md w-full bg-white dark:bg-zinc-900 rounded-xl shadow-lg p-10 text-center border border-zinc-200 dark:border-zinc-800">
          <h1 className="text-4xl font-bold text-blue-600 mb-4">Data Safe</h1>
          <p className="text-zinc-600 dark:text-zinc-400 mb-8">
            Secure your endpoints and monitor your cloud events in real-time.
          </p>
          
          <button
            onClick={() => loginWithRedirect()}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-lg transition-all"
          >
            Log In to Dashboard
          </button>
        </div>
      </div>
    );
  }

  // 3. LOGGED IN STATE: Show the "Home Page" (Dashboard)
  return (
    <div className="min-h-screen bg-white dark:bg-black p-8">
      {/* Header / Nav */}
      <header className="flex justify-between items-center mb-12 border-b border-zinc-200 dark:border-zinc-800 pb-4">
        <h2 className="text-2xl font-bold dark:text-white">Dashboard</h2>
        <div className="flex items-center gap-4">
          <span className="text-sm text-zinc-600 dark:text-zinc-400">
            Welcome, {user?.name}
          </span>
          <button
            onClick={() => logout({ logoutParams: { returnTo: window.location.origin } })}
            className="text-sm text-red-600 hover:text-red-700 font-medium"
          >
            Logout
          </button>
        </div>
      </header>

      {/* Events */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-12">
        {}
        <div className="flex flex-col items-center p-6 bg-zinc-50 dark:bg-zinc-900 rounded-xl border border-zinc-200 dark:border-zinc-800">
          <div className="w-24 h-24 rounded-full border-4 border-blue-500 flex items-center justify-center mb-4">
            <span className="text-3xl font-bold dark:text-white">12</span>
          </div>
          <span className="font-medium text-zinc-600 dark:text-zinc-400">Events</span>
        </div>

        {/* Unsecure Endpoints */}
        <div className="flex flex-col items-center p-6 bg-zinc-50 dark:bg-zinc-900 rounded-xl border border-zinc-200 dark:border-zinc-800">
          <div className="w-24 h-24 rounded-full border-4 border-red-500 flex items-center justify-center mb-4">
            <span className="text-3xl font-bold dark:text-white">3</span>
          </div>
          <span className="font-medium text-zinc-600 dark:text-zinc-400">Unsecure Endpoints</span>
        </div>

        {/* Total Endpoints Scanned */}
        <div className="flex flex-col items-center p-6 bg-zinc-50 dark:bg-zinc-900 rounded-xl border border-zinc-200 dark:border-zinc-800">
          <div className="w-24 h-24 rounded-full border-4 border-green-500 flex items-center justify-center mb-4">
            <span className="text-3xl font-bold dark:text-white">45</span>
          </div>
          <span className="font-medium text-zinc-600 dark:text-zinc-400">Total Scanned</span>
        </div>
      </div>

      {/* WIREFRAME CONTENT: Most Recent Items List */}
      <div className="w-full bg-zinc-50 dark:bg-zinc-900 rounded-xl border border-zinc-200 dark:border-zinc-800 p-6">
        <h3 className="text-lg font-semibold mb-4 dark:text-white">Most Recent Items</h3>
        <div className="space-y-4">
          {/* Replace this with real data later */}
          {[1, 2, 3].map((item) => (
            <div key={item} className="h-12 bg-white dark:bg-black rounded border border-zinc-200 dark:border-zinc-800 w-full"></div>
          ))}
        </div>
      </div>
    </div>
  );
}