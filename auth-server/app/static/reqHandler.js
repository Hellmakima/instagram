let csrfToken = null;

async function getCsrfToken() {
  const res = await fetch("/v1/auth/csrf-token", {
    credentials: "same-origin",
  });
  if (!res.ok) throw new Error(`CSRF fetch failed (${res.status})`);
  const data = await res.json();
  csrfToken = data.data.csrf_token;
  return csrfToken;
}

export async function apiRequest(url, options = {}, retry = true) {
  if (!csrfToken) await getCsrfToken();

  const headers = {
    "Content-Type": "application/json",
    "X-CSRF-Token": csrfToken,
    ...(options.headers || {}),
  };

  const res = await fetch(url, {
    ...options,
    headers,
    credentials: "same-origin",
  });

  if (res.status === 403 && retry) {
    // console.warn("CSRF token expired. Refreshing and retrying...");
    await getCsrfToken();
    return apiRequest(url, options, false);
  }

  let data;
  try {
    data = await res.json();
  } catch {
    data = { message: "Invalid JSON response" };
  }

  if (!res.ok) throw { status: res.status, data };
  return data;
}
