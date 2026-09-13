export async function checkApiHealth(apiBaseUrl: string): Promise<boolean> {
  try {
    const response = await fetch(`${apiBaseUrl}/health/live`);
    return response.ok;
  } catch {
    return false;
  }
}
