// src/lib/validators.ts
export function isEmailValid(email: string) {
  return /\S+@\S+\.\S+/.test(email);
}

export function isPasswordValid(password: string) {
  // len > 10 <30, must contain uppercase, lowercase, number, and special char
  return password.length > 10 && 
    password.length < 30 && 
    password.match(/[A-Z]/) && 
    password.match(/[a-z]/) && 
    password.match(/[0-9]/) && 
    password.match(/[!@#$%^&*(),.?":{}|<>]/);
}
