import { useEffect, useState } from "react";
import PastTable from "./PastTable";
import ScheduleTable from "./ScheduleTable";
import { ScheduledTradeResponse } from "../../../api/types";
import { getScheduled } from "../../../api/tradeApi";
import { nextMinute } from "../../../Utils/helper";

interface TablesProps {
  open: boolean;
}

export default function Tables({ open }: TablesProps) {
  const [scheduled, setScheduled] = useState<ScheduledTradeResponse[]>([]);
  const [past, setPast] = useState<ScheduledTradeResponse[]>([]);
  const [edtOpen, setEdtOpen] = useState(false);

  const getTrades = async () => {
    const response = await getScheduled();
    const temp: ScheduledTradeResponse[] = [];
    const temp2: ScheduledTradeResponse[] = [];
    response.data.forEach((trade) => {
      if (trade.status === "scheduled") temp.push(trade);
      else temp2.push(trade);
    });

    setScheduled(temp.reverse());
    setPast(temp2);
  };

  useEffect(() => {
    getTrades();
    const startPolling = () => {
      getTrades();
      const interval = setInterval(getTrades, 60000);
      return () => clearInterval(interval);
    };
    const timeout = setTimeout(() => {
      startPolling();
    }, nextMinute());
    return () => clearTimeout(timeout);
  }, []);

  useEffect(() => {
    getTrades();
  }, [edtOpen, open]);

  return (
    <div className="flex flex-1 justify-between bg-white">
      <ScheduleTable
        data={scheduled}
        setData={setScheduled}
        open={edtOpen}
        setOpen={setEdtOpen}
      />
      <PastTable data={past} />
    </div>
  );
}
