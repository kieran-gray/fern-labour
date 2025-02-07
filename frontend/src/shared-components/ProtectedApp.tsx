import { useEffect, useState, type ReactNode } from 'react';
import { hasAuthParams, useAuth } from 'react-oidc-context';
import { ErrorContainer } from './ErrorContainer/ErrorContainer.tsx';
import { PageLoading } from './PageLoading/PageLoading.tsx';

interface ProtectedAppProps {
  children: ReactNode;
}

export const ProtectedApp: React.FC<ProtectedAppProps> = (props) => {
  const { children } = props;

  const auth = useAuth();
  const [hasTriedSignin, setHasTriedSignin] = useState(false);

  /**
   * Do auto sign in.
   *
   * See {@link https://github.com/authts/react-oidc-context?tab=readme-ov-file#automatic-sign-in}
   */
  useEffect(() => {
    if (
      !(
        hasAuthParams() ||
        auth.isAuthenticated ||
        auth.activeNavigator ||
        auth.isLoading ||
        hasTriedSignin
      )
    ) {
      void auth.signinRedirect();
      setHasTriedSignin(true);
    }
  }, [auth, hasTriedSignin]);

  return (
    <>
      {auth.error ? (
        <ErrorContainer message={auth.error?.message} />
      ) : auth.isLoading ? (
        <>
          <PageLoading />
        </>
      ) : auth.isAuthenticated ? (
        children
      ) : (
        <ErrorContainer message="Unable to sign in" />
      )}
    </>
  );
};
