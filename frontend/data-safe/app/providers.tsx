'use client';

import { Auth0Provider } from "@auth0/auth0-react";
import { useEffect, useState } from "react";

export function Providers({ children }: { children: React.ReactNode }) {
  const [redirectUri, setRedirectUri] = useState<string>("");

  useEffect(() => {
    setRedirectUri(window.location.origin);
  }, []);

  if (!redirectUri) return <>{children}</>;

  return (
    <Auth0Provider
      domain="dev-t2e2x52h4gs4vmrb.us.auth0.com"
      clientId="qHrandEAgVyXanloFVlMcMrTaJApGUfO"
      authorizationParams={{ redirect_uri: redirectUri }}
    >
      {children}
    </Auth0Provider>
  );
}