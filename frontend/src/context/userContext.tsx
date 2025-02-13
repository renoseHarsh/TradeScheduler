import React, {
  createContext,
  ReactNode,
  useContext,
  useEffect,
  useState,
} from "react";

import { UserData } from "../api/types";
import { getUser } from "../api/authApi";

interface UserContextType {
  user: UserData | null;
  setUser: React.Dispatch<React.SetStateAction<UserData | null>>;
}

const UserContext = createContext<UserContextType | null>(null);

export const useUserContext = () => {
  const context = useContext(UserContext);
  if (!context) {
    throw new Error("useUserContext must be used within a UserProvider");
  }
  return context;
};

type UserProviderProps = {
  children: ReactNode;
};

const UserProvider = ({ children }: UserProviderProps) => {
  const [user, setUser] = useState<UserData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchUser = async () => {
      const response = await getUser();
      if (response.status == 200) setUser(response.data);
      setLoading(false);
    };

    fetchUser();
  }, []);

  return (
    <>
      {loading ? (
        <div className="flex h-screen w-screen items-center justify-center">
          <span className="loading loading-spinner loading-lg"></span>
        </div>
      ) : (
        <UserContext.Provider value={{ user, setUser }}>
          {children}
        </UserContext.Provider>
      )}
    </>
  );
};

export default UserProvider;
