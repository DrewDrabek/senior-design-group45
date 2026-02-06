'use client';

import { Auth0Provider } from "@auth0/auth0-react";
import { useEffect, useState } from "react";

export function Providers({ children }: { children: React.ReactNode }) {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);
  if (!mounted) return null;

  return (
    <Auth0Provider
      domain="dev-t2e2x52h4gs4vmrb.us.auth0.com"
      clientId="qHrandEAgVyXanloFVlMcMrTaJApGUfO"
      authorizationParams={{
        redirect_uri: window.location.origin,
      }}
      // This ensures the cache is stored in local storage, preventing login loss on refresh
      cacheLocation="localstorage"
    >
      {children}
    </Auth0Provider>
  );
}