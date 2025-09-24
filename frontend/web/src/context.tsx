import { createContext } from 'react';

export interface AuthState { user: any | null; loading: boolean; }
export const AuthCtx = createContext<{state: AuthState; setState: (s: AuthState) => void}>({state: {user: null, loading: true}, setState: () => {}});
