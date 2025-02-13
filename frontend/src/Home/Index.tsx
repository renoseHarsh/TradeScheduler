import Navbar from "./components/Nav/Navbar";
import Tables from "./components/Dashboards.tsx/Tables";
import { useState } from "react";

export default function Index() {
  const [open, setOpen] = useState(false);
  return (
    <div className="flex h-full flex-col">
      <Navbar scheduleModal={open} setScheduleModal={setOpen} />
      <Tables open={open} />
    </div>
  );
}