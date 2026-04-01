import { AuthCard } from '@/components/auth/auth-card';

export default function LoginPage() {
  return (
    <main className='flex min-h-screen items-center justify-center px-6'>
      <AuthCard mode='login' />
    </main>
  );
}
