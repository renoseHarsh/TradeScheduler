export const nextMinute = () => {
  const now = new Date();
  const onlyMinute = new Date(now);
  onlyMinute.setSeconds(0);
  onlyMinute.setMilliseconds(0);
  return 60000 - (now.getTime() - onlyMinute.getTime()) + 5000;
};
