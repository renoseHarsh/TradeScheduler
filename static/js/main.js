const changeUnits = () => {
  const is_percent = document.getElementById("percentage-checkbox");
  const qauntatiy = document.getElementById("quantatiy_input");
  if (is_percent.checked) {
    qauntatiy.placeholder = "Percentage";
    qauntatiy.max = 100;
  } else {
    qauntatiy.placeholder = "Units";
    qauntatiy.max = "";
  }
};
