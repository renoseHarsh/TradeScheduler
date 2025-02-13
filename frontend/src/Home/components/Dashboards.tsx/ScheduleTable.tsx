import React, { useState } from "react";
import EditScheduleModal from "./EditScheduleModal";
import { ScheduledTradeResponse } from "../../../api/types";
import { deleteScheduled } from "../../../api/tradeApi";

interface ScheduleTableProps {
  data: ScheduledTradeResponse[];
  open: boolean;
  setData: React.Dispatch<React.SetStateAction<ScheduledTradeResponse[]>>;
  setOpen: (value: boolean) => void;
}

export default function ScheduleTable({
  data,
  open,
  setData,
  setOpen,
}: ScheduleTableProps) {
  const [selected, setSelected] = useState<
    ScheduledTradeResponse | undefined
  >();

  const onDelete = async (id: string) => {
    await deleteScheduled(id);
    setData((prev) => prev.filter((itme) => itme.id != id));
  };

  return (
    <div className="flex flex-1 flex-col items-start gap-2 bg-[#a5a4a4] p-4 hover:cursor-default">
      {/* Counter */}
      <div className="mx-auto flex flex-col items-center rounded-lg bg-blue-600 px-4 text-white shadow-md">
        <span className="text-lg font-semibold">Scheduled</span>
        <span className="text-2xl font-bold">{data.length}</span>
      </div>
      {/* Table */}
      <div className="max-table-height self-center overflow-x-auto rounded bg-white shadow-lg">
        {/* Edit Modal */}
        {open && (
          <EditScheduleModal
            onClose={() => setOpen(false)}
            selected={selected}
          />
        )}
        <table className="table table-pin-rows">
          {/* Head */}
          <thead className="text-white">
            <tr>
              <th>Pair</th>
              <th>
                Units/
                <br />
                Percentage
              </th>
              <th>
                Take
                <br />
                Profit
              </th>
              <th>
                Stop
                <br />
                Loss
              </th>
              <th>
                Scheduled
                <br />
                Time
              </th>
              <th>Account</th>
              <th></th>
              <th></th>
            </tr>
          </thead>
          {/* Body */}
          <tbody className="text-gray-600">
            {data.map((item, index) => (
              <tr key={index}>
                <td
                  className={`font-medium text-green-600 ${item.action === "sell" ? "text-red-600" : "text-green-600"}`}
                >
                  {item.pair.replace("_", "")}
                </td>
                <td>
                  {item.units || item.percentage}
                  {item.percentage && "%"}
                </td>
                <td className="whitespace-nowrap">{item.take_profit} pip(s)</td>
                <td className="whitespace-nowrap">{item.stop_loss} pip(s)</td>
                <td>
                  <span className="whitespace-nowrap">
                    {item.scheduled_time.split("T")[0]}
                  </span>
                  <br />
                  {item.scheduled_time.split("T")[1]}
                </td>
                <td>
                  {item.account_type}
                  <br />
                  <span
                    className="tooltip whitespace-nowrap"
                    data-tip={item.account_id}
                  >
                    {item.account_id.split("-")[2]}
                  </span>
                </td>
                <td>
                  <button
                    type="button"
                    onClick={() => {
                      setOpen(true);
                      setSelected(item);
                    }}
                    className="rounded-lg bg-green-500 px-4 py-2 text-white shadow transition-transform duration-200 hover:bg-green-600 active:scale-95 active:bg-green-700"
                  >
                    Edit
                  </button>
                </td>
                <td>
                  <button
                    type="button"
                    className="rounded-lg bg-red-500 px-4 py-2 text-white shadow transition-transform duration-200 hover:bg-red-600 active:scale-95 active:bg-red-700"
                    onClick={() => onDelete(item.id)}
                  >
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
