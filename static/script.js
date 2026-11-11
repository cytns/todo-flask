const tasks = document.querySelectorAll("[data-task-id]");
const columns = document.querySelectorAll("[data-status]");

tasks.forEach(function (task) {
  task.addEventListener("dragstart", function (event) {
    event.dataTransfer.setData("text/plain", task.dataset.taskId);
  });
});

columns.forEach(function (column) {
  column.addEventListener("dragover", function (event) {
    event.preventDefault();
  });

  column.addEventListener("drop", function (event) {
    event.preventDefault();
    const taskId = event.dataTransfer.getData("text/plain");
    const status = column.dataset.status;
    if (!taskId) return;

    fetch("/move/" + taskId, {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: "status=" + encodeURIComponent(status)
    })
      .then(function (response) {
        if (!response.ok) throw new Error();
        window.location.reload();
      })
      .catch(function () {
        alert("Не удалось переместить задачу. Попробуйте ещё раз.");
      });
  });
});
