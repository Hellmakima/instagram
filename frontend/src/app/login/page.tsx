"use client"; // This directive is for App Router to make it a Client Component

import { useState } from 'react';
import { useRouter } from 'next/navigation'; // For App Router
// import { useRouter } from 'next/router'; // For Pages Router

export default function LoginPage() {
  const [showRegisterForm, setShowRegisterForm] = useState(false);
  const router = useRouter();

  const handleLogin = async (e: any) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const username:any = formData.get('username');
    const password:any = formData.get('password');

    try {
      const params = new URLSearchParams();
      params.append('username', username);
      params.append('password', password);

      const response = await fetch('/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: params,
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(errorText);
      }
      const result = await response.json();
      localStorage.setItem('access_token', result.access_token);
      localStorage.setItem('refresh_token', result.refresh_token);
      router.push('/me'); // Redirect to the profile page
    } catch (error: any) {
      console.error('Login error:', error);
      alert('Login failed: ' + error.message);
    }
  };

  const handleRegister = async (e: any) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const username = formData.get('username');
    const password = formData.get('password');

    try {
      const response = await fetch('/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }),
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(errorText);
      }
      const result = await response.json();
      localStorage.setItem('access_token', result.access_token);
      localStorage.setItem('refresh_token', result.refresh_token);
      router.push('/me'); // Redirect to the profile page
    } catch (error: any) {
      alert('Registration failed: ' + error.message);
    }
  };

  return (
    <div style={{ fontFamily: 'Arial', maxWidth: '400px', margin: '0 auto', padding: '20px' }}>
      <div style={{ display: 'flex', marginBottom: '20px' }} className="tabs">
        <button onClick={() => setShowRegisterForm(false)} style={{ flex: 1, padding: '10px' }}>Login</button>
        <button onClick={() => setShowRegisterForm(true)} style={{ flex: 1, padding: '10px' }}>Register</button>
      </div>

      {!showRegisterForm ? (
        <form onSubmit={handleLogin} style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
          <h2>Login</h2>
          <input type="text" name="username" placeholder="Username" required style={{ padding: '8px' }} />
          <input type="password" name="password" placeholder="Password" required style={{ padding: '8px' }} />
          <button type="submit" style={{ padding: '8px' }}>Login</button>
        </form>
      ) : (
        <form onSubmit={handleRegister} style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
          <h2>Register</h2>
          <input type="text" name="username" placeholder="Username" required style={{ padding: '8px' }} />
          <input type="password" name="password" placeholder="Password" required style={{ padding: '8px' }} />
          <button type="submit" style={{ padding: '8px' }}>Register</button>
        </form>
      )}
    </div>
  );
}