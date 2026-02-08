import { Suspense } from 'react';
// import VerifyEmailClient from './verify-client';
import VerifyEmailPage from './verify-client';

export const dynamic = 'force-dynamic';

export default function Page() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <VerifyEmailPage />
    </Suspense>
  );
}
