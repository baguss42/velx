import { useEffect, useState } from "react";

import { checkApiHealth } from "./api/health";
import { ChatShell } from "./components/ChatShell";
import type { ApiStatus } from "./types/api";

const apiBaseUrl = import.meta.env.VITE_API_BASE_URL ?? "/api";

export function App() {
  const [apiStatus, setApiStatus] = useState<ApiStatus>("checking");

  useEffect(() => {
    let isCurrent = true;

    checkApiHealth(apiBaseUrl).then((isHealthy) => {
      if (isCurrent) {
        setApiStatus(isHealthy ? "online" : "offline");
      }
    });

    return () => {
      isCurrent = false;
    };
  }, []);

  return <ChatShell apiStatus={apiStatus} />;
}
