'use client';

import { useAuth0 } from "@auth0/auth0-react";
import { useRouter } from "next/navigation";
import { ReactNode } from "react";
import Link from "next/link";

export default function DashboardLayout({
    children,
}: {
    children: ReactNode;
}) {
    const { isAuthenticated, isLoading, loginWithRedirect, logout, user } = useAuth0();
    const router = useRouter();

    if (isLoading) {
        return (
            <div className="flex min-h-screen items-center justify-center">
                Loading...
            </div>
        );
    }

    if (!isAuthenticated) {
        loginWithRedirect();
        return null;
    }

    return (
        <div className="min-h-screen flex bg-white dark:bg-black">

            {/* Sidebar */}
            <aside className="w-64 bg-zinc-100 dark:bg-zinc-900 border-r border-zinc-200 dark:border-zinc-800 p-6">
                <h2 className="text-xl font-bold mb-8 dark:text-white">
                    Data Safe
                </h2>

                <nav className="space-y-4">
                    <Link
                        href="http://localhost:3000/"
                        className="block text-left w-full hover:text-blue-600 dark:text-zinc-300"
                    >
                        Dashboard
                    </Link>

                    <Link
                        href="/dashboard/events"
                        className="block text-left w-full hover:text-blue-600 dark:text-zinc-300"
                    >
                        Events
                    </Link>

                    <Link
                        href="/dashboard/unsecure"
                        className="block text-left w-full hover:text-blue-600 dark:text-zinc-300"
                    >
                        Unsecure Endpoints
                    </Link>

                    <Link
                        href="/dashboard/endpoints"
                        className="block text-left w-full hover:text-blue-600 dark:text-zinc-300"
                    >
                        Endpoint Management
                    </Link>
                </nav>

                <div className="mt-12 text-sm dark:text-zinc-400">
                    Logged in as:
                    <div className="font-medium">{user?.name}</div>

                    <button
                        onClick={() =>
                            logout({ logoutParams: { returnTo: window.location.origin } })
                        }
                        className="mt-4 text-red-600 hover:underline"
                    >
                        Logout
                    </button>
                </div>
            </aside>

            {/* Main Content */}
            <main className="flex-1 p-8">{children}</main>
        </div>
    );
}