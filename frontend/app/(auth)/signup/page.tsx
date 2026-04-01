import { AuthCard } from '@/components/auth/auth-card';

export default function SignupPage() {
  return (
    <main className='flex min-h-screen items-center justify-center px-6'>
      <AuthCard mode='signup' />
    </main>
  );
}
