"use client"; // This directive is for App Router to make it a Client Component

import { useEffect, useState, useCallback } from 'react';
import { useRouter } from 'next/navigation'; // For App Router
// import { useRouter } from 'next/router'; // For Pages Router
interface UserProfile {
  username: string;
  email?: string; // email is optional
}
export default function MePage() {
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const router = useRouter();

  const redirectToLogin = useCallback(() => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    router.push('/login');
  }, [router]);

  const manualRefresh = async () => {
    const refresh_token = localStorage.getItem('refresh_token');
    if (!refresh_token) return alert("No refresh token found!");

    try {
      const response = await fetch('/auth/refresh', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          refresh_token: refresh_token,
          token_type: 'Bearer'
        })
      });

      if (!response.ok) throw new Error(await response.text());

      const result = await response.json();
      localStorage.setItem('access_token', result.access_token);
      localStorage.setItem('refresh_token', result.refresh_token);

      alert("Token refreshed successfully!");
      // Optionally reload profile after refreshing token
      loadProfile();
    } catch (err: any) {
      console.error('Error refreshing token:', err);
      alert("Failed to refresh token: " + err.message);
      redirectToLogin();
    }
  };

  const loadProfile = useCallback(async () => {
    let token = localStorage.getItem('access_token');
    if (!token) return redirectToLogin();

    try {
      let response = await fetch('/user/me', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.status === 401) {
        const refresh_token = localStorage.getItem('refresh_token');
        if (!refresh_token) return redirectToLogin();

        const refreshResponse = await fetch('/auth/refresh', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            refresh_token: refresh_token,
            token_type: 'Bearer'
          })
        });

        if (!refreshResponse.ok) {
          alert('Failed to refresh token during automatic refresh. Please log in again.');
          return redirectToLogin();
        }

        const result = await refreshResponse.json();
        localStorage.setItem('access_token', result.access_token);
        localStorage.setItem('refresh_token', result.refresh_token); // in case it rotates

        // Retry loading profile with the new token
        token = result.access_token; // Update token for the retry
        response = await fetch('/user/me', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        if (!response.ok) throw new Error(await response.text());
      }

      if (!response.ok) throw new Error(await response.text());
      const user = await response.json();
      setProfile(user);
    } catch (error: any) {
      console.error('Error loading profile:', error);
      alert('Failed to load profile: ' + error.message);
      redirectToLogin();
    }
  }, [redirectToLogin]);

  async function logout() {
    const refresh_token = localStorage.getItem('refresh_token');
    await fetch('/auth/logout', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        refresh_token: refresh_token,
        token_type: 'Bearer'
      })
    });
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    router.push('/login');
  }

  useEffect(() => {
    loadProfile();
  }, [loadProfile]);

  return (
    <div style={{ fontFamily: 'Arial', maxWidth: '600px', margin: '0 auto', padding: '20px' }}>
      <h1>My Profile</h1>
      <div id="profile" style={{ marginTop: '20px', padding: '20px', border: '1px solid #ddd' }}>
        {profile ? (
          <>
            <p><strong>Username:</strong> {profile.username}</p>
            <p><strong>Email:</strong> {profile.email || 'Not provided'}</p>
          </>
        ) : (
          'Loading...'
        )}
      </div>
      <button onClick={logout} style={{ padding: '8px 12px', marginTop: '10px' }}>Logout</button>
      <button onClick={manualRefresh} style={{ padding: '8px 12px', marginTop: '10px', marginLeft: '10px' }}>Refresh Token</button>
    </div>
  );
}