import { useState } from "react";
import TokenModal from "./TokenModal";
import ScheduleModal from "./ScheduleModal";
import { useUserContext } from "../../../context/userContext";
import { logoutUser } from "../../../api/authApi";

interface NavbarProps {
  scheduleModal: boolean;
  setScheduleModal: (value: boolean) => void;
}

export default function Navbar({
  scheduleModal,
  setScheduleModal,
}: NavbarProps) {
  const [tokenModal, setTokenModal] = useState(false);

  const { user, setUser } = useUserContext();

  const logout = async () => {
    setUser(null);
    await logoutUser();
  };

  return (
    <div className="flex h-20 items-center justify-between bg-[#014487] px-10 font-sans text-white">
      <p className="text-bold text-2xl hover:cursor-default">
        {user?.username}
      </p>
      <div className="flex h-12 gap-2">
        <button
          className="rounded-md bg-[#28A745] px-3 text-center transition-all duration-200 hover:bg-[#218838] active:scale-95 active:bg-[#1E7E34]"
          onClick={() => setScheduleModal(true)}
        >
          Schedule
          <br />
          Trade
        </button>
        {scheduleModal && (
          <ScheduleModal onClose={() => setScheduleModal(false)} />
        )}

        <button
          className="rounded-md bg-[#007BFF] px-3 transition-all duration-200 hover:bg-[#0056b3] active:scale-95 active:bg-[#004085]"
          onClick={() => setTokenModal(true)}
        >
          Manage
          <br />
          Token
        </button>
        {tokenModal && <TokenModal onClose={() => setTokenModal(false)} />}
        <button
          className="rounded-md bg-[#FF7043] px-3 transition-all duration-200 hover:bg-[#E64A19] active:scale-95 active:bg-[#D84315]"
          onClick={logout}
        >
          Logout
        </button>
      </div>
    </div>
  );
}
