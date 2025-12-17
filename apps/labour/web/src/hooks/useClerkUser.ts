import { useUser } from '@clerk/clerk-react';

export function useClerkUser() {
  const { user: clerkUser, isLoaded } = useUser();

  if (!clerkUser || !isLoaded) {
    return { user: null, isLoaded };
  }

  const user = {
    ...clerkUser,
    sub: clerkUser.id,
    email: clerkUser.primaryEmailAddress?.emailAddress,
    email_address: clerkUser.primaryEmailAddress?.emailAddress,
    given_name: clerkUser.firstName,
    family_name: clerkUser.lastName,
    first_name: clerkUser.firstName,
    last_name: clerkUser.lastName,
    name: clerkUser.fullName,
    phone_number: clerkUser.primaryPhoneNumber?.phoneNumber,
  };

  return { user, isLoaded };
}
