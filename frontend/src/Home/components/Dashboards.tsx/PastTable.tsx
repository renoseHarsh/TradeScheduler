import { useEffect, useState } from "react";
import { ScheduledTradeResponse } from "../../../api/types";

interface PastTableProps {
  data: ScheduledTradeResponse[];
}

export default function PastTable({ data }: PastTableProps) {
  const [info, setInfo] = useState<{ success: number; failed: number }>({
    success: 0,
    failed: 0,
  });

  useEffect(() => {
    let success = 0;
    let failed = 0;
    data.forEach((item) => {
      if (item.status == "success") success++;
      else failed++;
    });
    setInfo({ success, failed });
  }, [data]);

  return (
    <div className="flex flex-1 flex-col items-start gap-2 bg-[#a5a4a4] p-4 hover:cursor-default">
      {/* Counter */}
      <div className="mx-auto flex gap-2">
        <div className="mx-auto flex flex-col items-center rounded-lg bg-green-500 px-4 text-white shadow-md">
          <span className="text-lg font-semibold">Successful</span>
          <span className="text-2xl font-bold">{info.success.toString()}</span>
        </div>
        <div className="mx-auto flex flex-col items-center rounded-lg bg-red-500 px-4 text-white shadow-md">
          <span className="text-lg font-semibold">Failed</span>
          <span className="text-2xl font-bold">{info.failed.toString()}</span>
        </div>
      </div>
      {/* Table */}
      <div className="max-table-height self-center overflow-x-auto rounded bg-white shadow-lg">
        <table className="table table-pin-rows">
          {/* Head */}
          <thead className="text-white">
            <tr>
              <th>Pair</th>
              <th>
                Units/
                <br />%
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
              <th>Status</th>
              <th>Account</th>
            </tr>
          </thead>
          {/* Body */}
          <tbody className="text-gray-600">
            {data.map((item, index) => (
              <tr key={index}>
                <td
                  className={`font-medium text-green-600 ${item.action == "sell" ? "text-red-600" : "text-gre"}`}
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
                  {item.status == "success" ? (
                    <>
                      <span className="whitespace-nowrap">
                        {item.scheduled_time.split("T")[0]}
                      </span>
                      <br />
                      {item.scheduled_time.split("T")[1]}
                    </>
                  ) : item.status.length > 25 ? (
                    <span
                      className="tooltip tooltip-left"
                      data-tip={item.status}
                    >
                      {item.status.slice(0, 25)} ...
                    </span>
                  ) : (
                    item.status
                  )}
                </td>
                <td>
                  {item.account_type}
                  <br />
                  <span
                    className="tooltip tooltip-left whitespace-nowrap"
                    data-tip={item.account_id}
                  >
                    {item.account_id.split("-")[2]}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
